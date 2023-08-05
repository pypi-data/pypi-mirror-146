import logging

from pip._vendor.packaging.utils import canonicalize_name

from pip._internal.exceptions import (
    DistributionNotFound,
    InstallationError,
    InstallationSubprocessError,
    MetadataInconsistent,
    UnsupportedPythonVersion,
    UnsupportedWheel,
)
from pip._internal.models.wheel import Wheel
from pip._internal.req.req_install import InstallRequirement
from pip._internal.utils.compatibility_tags import get_supported
from pip._internal.utils.hashes import Hashes
from pip._internal.utils.misc import (
    dist_in_site_packages,
    dist_in_usersite,
    get_installed_distributions,
)
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.virtualenv import running_under_virtualenv

from .base import Constraint
from .candidates import (
    AlreadyInstalledCandidate,
    EditableCandidate,
    ExtrasCandidate,
    LinkCandidate,
    RequiresPythonCandidate,
)
from .found_candidates import FoundCandidates
from .requirements import (
    ExplicitRequirement,
    RequiresPythonRequirement,
    SpecifierRequirement,
    UnsatisfiableRequirement,
)

if MYPY_CHECK_RUNNING:
    from typing import (
        Dict,
        FrozenSet,
        Iterable,
        Iterator,
        List,
        Optional,
        Sequence,
        Set,
        Tuple,
        TypeVar,
    )

    from pip._vendor.packaging.specifiers import SpecifierSet
    from pip._vendor.packaging.version import _BaseVersion
    from pip._vendor.pkg_resources import Distribution
    from pip._vendor.resolvelib import ResolutionImpossible

    from pip._internal.cache import CacheEntry, WheelCache
    from pip._internal.index.package_finder import PackageFinder
    from pip._internal.models.link import Link
    from pip._internal.operations.prepare import RequirementPreparer
    from pip._internal.resolution.base import InstallRequirementProvider

    from .base import Candidate, Requirement
    from .candidates import BaseCandidate

    C = TypeVar("C")
    Cache = Dict[Link, C]
    VersionCandidates = Dict[_BaseVersion, Candidate]


logger = logging.getLogger(__name__)


class Factory(object):
    def __init__(
        self,
        finder,  # type: PackageFinder
        preparer,  # type: RequirementPreparer
        make_install_req,  # type: InstallRequirementProvider
        wheel_cache,  # type: Optional[WheelCache]
        use_user_site,  # type: bool
        force_reinstall,  # type: bool
        ignore_installed,  # type: bool
        ignore_requires_python,  # type: bool
        py_version_info=None,  # type: Optional[Tuple[int, ...]]
    ):
        # type: (...) -> None
        self._finder = finder
        self.preparer = preparer
        self._wheel_cache = wheel_cache
        self._python_candidate = RequiresPythonCandidate(py_version_info)
        self._make_install_req_from_spec = make_install_req
        self._use_user_site = use_user_site
        self._force_reinstall = force_reinstall
        self._ignore_requires_python = ignore_requires_python

        self._build_failures = {}  # type: Cache[InstallationError]
        self._link_candidate_cache = {}  # type: Cache[LinkCandidate]
        self._editable_candidate_cache = {}  # type: Cache[EditableCandidate]
        self._installed_candidate_cache = {
        }  # type: Dict[str, AlreadyInstalledCandidate]

        if not ignore_installed:
            self._installed_dists = {
                canonicalize_name(dist.project_name): dist
                for dist in get_installed_distributions(local_only=False)
            }
        else:
            self._installed_dists = {}

    @property
    def force_reinstall(self):
        # type: () -> bool
        return self._force_reinstall

    def _make_candidate_from_dist(
        self,
        dist,  # type: Distribution
        extras,  # type: FrozenSet[str]
        template,  # type: InstallRequirement
    ):
        # type: (...) -> Candidate
        try:
            base = self._installed_candidate_cache[dist.key]
        except KeyError:
            base = AlreadyInstalledCandidate(dist, template, factory=self)
            self._installed_candidate_cache[dist.key] = base
        if extras:
            return ExtrasCandidate(base, extras)
        return base

    def _make_candidate_from_link(
        self,
        link,  # type: Link
        extras,  # type: FrozenSet[str]
        template,  # type: InstallRequirement
        name,  # type: Optional[str]
        version,  # type: Optional[_BaseVersion]
    ):
        # type: (...) -> Optional[Candidate]
        # TODO: Check already installed candidate, and use it if the link and
        # editable flag match.

        if link in self._build_failures:
            # We already tried this candidate before, and it does not build.
            # Don't bother trying again.
            return None

        if template.editable:
            if link not in self._editable_candidate_cache:
                try:
                    self._editable_candidate_cache[link] = EditableCandidate(
                        link, template, factory=self,
                        name=name, version=version,
                    )
                except (InstallationSubprocessError, MetadataInconsistent) as e:
                    logger.warning("Discarding %s. %s", link, e)
                    self._build_failures[link] = e
                    return None
            base = self._editable_candidate_cache[link]  # type: BaseCandidate
        else:
            if link not in self._link_candidate_cache:
                try:
                    self._link_candidate_cache[link] = LinkCandidate(
                        link, template, factory=self,
                        name=name, version=version,
                    )
                except (InstallationSubprocessError, MetadataInconsistent) as e:
                    logger.warning("Discarding %s. %s", link, e)
                    self._build_failures[link] = e
                    return None
            base = self._link_candidate_cache[link]

        if extras:
            return ExtrasCandidate(base, extras)
        return base

    def _iter_found_candidates(
        self,
        ireqs,  # type: Sequence[InstallRequirement]
        specifier,  # type: SpecifierSet
        hashes,  # type: Hashes
        prefers_installed,  # type: bool
    ):
        # type: (...) -> Iterable[Candidate]
        if not ireqs:
            return ()

        # The InstallRequirement implementation requires us to give it a
        # "template". Here we just choose the first requirement to represent
        # all of them.
        # Hopefully the Project model can correct this mismatch in the future.
        template = ireqs[0]
        name = canonicalize_name(template.req.name)

        extras = frozenset()  # type: FrozenSet[str]
        for ireq in ireqs:
            specifier &= ireq.req.specifier
            hashes &= ireq.hashes(trust_internet=False)
            extras |= frozenset(ireq.extras)

        # Get the installed version, if it matches, unless the user
        # specified `--force-reinstall`, when we want the version from
        # the index instead.
        installed_candidate = None
        if not self._force_reinstall and name in self._installed_dists:
            installed_dist = self._installed_dists[name]
            if specifier.contains(installed_dist.version, prereleases=True):
                installed_candidate = self._make_candidate_from_dist(
                    dist=installed_dist,
                    extras=extras,
                    template=template,
                )

        def iter_index_candidates():
            # type: () -> Iterator[Candidate]
            result = self._finder.find_best_candidate(
                project_name=name,
                specifier=specifier,
                hashes=hashes,
            )
            icans = list(result.iter_applicable())

            # PEP 592: Yanked releases must be ignored unless only yanked
            # releases can satisfy the version range. So if this is false,
            # all yanked icans need to be skipped.
            all_yanked = all(ican.link.is_yanked for ican in icans)

            # PackageFinder returns earlier versions first, so we reverse.
            versions_found = set()  # type: Set[_BaseVersion]
            for ican in reversed(icans):
                if not all_yanked and ican.link.is_yanked:
                    continue
                if ican.version in versions_found:
                    continue
                candidate = self._make_candidate_from_link(
                    link=ican.link,
                    extras=extras,
                    template=template,
                    name=name,
                    version=ican.version,
                )
                if candidate is None:
                    continue
                yield candidate
                versions_found.add(ican.version)

        return FoundCandidates(
            iter_index_candidates,
            installed_candidate,
            prefers_installed,
        )

    def find_candidates(
        self,
        requirements,  # type: Sequence[Requirement]
        constraint,  # type: Constraint
        prefers_installed,  # type: bool
    ):
        # type: (...) -> Iterable[Candidate]
        explicit_candidates = set()  # type: Set[Candidate]
        ireqs = []  # type: List[InstallRequirement]
        for req in requirements:
            cand, ireq = req.get_candidate_lookup()
            if cand is not None:
                explicit_candidates.add(cand)
            if ireq is not None:
                ireqs.append(ireq)

        # If none of the requirements want an explicit candidate, we can ask
        # the finder for candidates.
        if not explicit_candidates:
            return self._iter_found_candidates(
                ireqs,
                constraint.specifier,
                constraint.hashes,
                prefers_installed,
            )

        return (
            c for c in explicit_candidates
            if constraint.is_satisfied_by(c)
            and all(req.is_satisfied_by(c) for req in requirements)
        )

    def make_requirement_from_install_req(self, ireq, requested_extras):
        # type: (InstallRequirement, Iterable[str]) -> Optional[Requirement]
        if not ireq.match_markers(requested_extras):
            logger.info(
                "Ignoring %s: markers '%s' don't match your environment",
                ireq.name, ireq.markers,
            )
            return None
        if not ireq.link:
            return SpecifierRequirement(ireq)
        if ireq.link.is_wheel:
            wheel = Wheel(ireq.link.filename)
            if not wheel.supported(self._finder.target_python.get_tags()):
                msg = "{} is not a supported wheel on this platform.".format(
                    wheel.filename,
                )
                raise UnsupportedWheel(msg)
        cand = self._make_candidate_from_link(
            ireq.link,
            extras=frozenset(ireq.extras),
            template=ireq,
            name=canonicalize_name(ireq.name) if ireq.name else None,
            version=None,
        )
        if cand is None:
            # There's no way we can satisfy a URL requirement if the underlying
            # candidate fails to build. An unnamed URL must be user-supplied, so
            # we fail eagerly. If the URL is named, an unsatisfiable requirement
            # can make the resolver do the right thing, either backtrack (and
            # maybe find some other requirement that's buildable) or raise a
            # ResolutionImpossible eventually.
            if not ireq.name:
                raise self._build_failures[ireq.link]
            return UnsatisfiableRequirement(canonicalize_name(ireq.name))
        return self.make_requirement_from_candidate(cand)

    def make_requirement_from_candidate(self, candidate):
        # type: (Candidate) -> ExplicitRequirement
        return ExplicitRequirement(candidate)

    def make_requirement_from_spec(
        self,
        specifier,  # type: str
        comes_from,  # type: InstallRequirement
        requested_extras=(),  # type: Iterable[str]
    ):
        # type: (...) -> Optional[Requirement]
        ireq = self._make_install_req_from_spec(specifier, comes_from)
        return self.make_requirement_from_install_req(ireq, requested_extras)

    def make_requires_python_requirement(self, specifier):
        # type: (Optional[SpecifierSet]) -> Optional[Requirement]
        if self._ignore_requires_python or specifier is None:
            return None
        return RequiresPythonRequirement(specifier, self._python_candidate)

    def get_wheel_cache_entry(self, link, name):
        # type: (Link, Optional[str]) -> Optional[CacheEntry]
        """Look up the link in the wheel cache.

        If ``preparer.require_hashes`` is True, don't use the wheel cache,
        because cached wheels, always built locally, have different hashes
        than the files downloaded from the index server and thus throw false
        hash mismatches. Furthermore, cached wheels at present have
        nondeterministic contents due to file modification times.
        """
        if self._wheel_cache is None or self.preparer.require_hashes:
            return None
        return self._wheel_cache.get_cache_entry(
            link=link,
            package_name=name,
            supported_tags=get_supported(),
        )

    def get_dist_to_uninstall(self, candidate):
        # type: (Candidate) -> Optional[Distribution]
        # TODO: Are there more cases this needs to return True? Editable?
        dist = self._installed_dists.get(candidate.name)
        if dist is None:  # Not installed, no uninstallation required.
            return None

        # We're installing into global site. The current installation must
        # be uninstalled, no matter it's in global or user site, because the
        # user site installation has precedence over global.
        if not self._use_user_site:
            return dist

        # We're installing into user site. Remove the user site installation.
        if dist_in_usersite(dist):
            return dist

        # We're installing into user site, but the installed incompatible
        # package is in global site. We can't uninstall that, and would let
        # the new user installation to "shadow" it. But shadowing won't work
        # in virtual environments, so we error out.
        if running_under_virtualenv() and dist_in_site_packages(dist):
            raise InstallationError(
                "Will not install to the user site because it will "
                "lack sys.path precedence to {} in {}".format(
                    dist.project_name, dist.location,
                )
            )
        return None

    def _report_requires_python_error(
        self,
        requirement,  # type: RequiresPythonRequirement
        template,  # type: Candidate
    ):
        # type: (...) -> UnsupportedPythonVersion
        message_format = (
            "Package {package!r} requires a different Python: "
            "{version} not in {specifier!r}"
        )
        message = message_format.format(
            package=template.name,
            version=self._python_candidate.version,
            specifier=str(requirement.specifier),
        )
        return UnsupportedPythonVersion(message)

    def get_installation_error(self, e):
        # type: (ResolutionImpossible) -> InstallationError

        assert e.causes, "Installation error reported with no cause"

        # If one of the things we can't solve is "we need Python X.Y",
        # that is what we report.
        for cause in e.causes:
            if isinstance(cause.requirement, RequiresPythonRequirement):
                return self._report_requires_python_error(
                    cause.requirement,
                    cause.parent,
                )

        # Otherwise, we have a set of causes which can't all be satisfied
        # at once.

        # The simplest case is when we have *one* cause that can't be
        # satisfied. We just report that case.
        if len(e.causes) == 1:
            req, parent = e.causes[0]
            if parent is None:
                req_disp = str(req)
            else:
                req_disp = '{} (from {})'.format(req, parent.name)
            logger.critical(
                "Could not find a version that satisfies the requirement %s",
                req_disp,
            )
            return DistributionNotFound(
                'No matching distribution found for {}'.format(req)
            )

        # OK, we now have a list of requirements that can't all be
        # satisfied at once.

        # A couple of formatting helpers
        def text_join(parts):
            # type: (List[str]) -> str
            if len(parts) == 1:
                return parts[0]

            return ", ".join(parts[:-1]) + " and " + parts[-1]

        def describe_trigger(parent):
            # type: (Candidate) -> str
            ireq = parent.get_install_requirement()
            if not ireq or not ireq.comes_from:
                return "{}=={}".format(parent.name, parent.version)
            if isinstance(ireq.comes_from, InstallRequirement):
                return str(ireq.comes_from.name)
            return str(ireq.comes_from)

        triggers = set()
        for req, parent in e.causes:
            if parent is None:
                # This is a root requirement, so we can report it directly
                trigger = req.format_for_error()
            else:
                trigger = describe_trigger(parent)
            triggers.add(trigger)

        if triggers:
            info = text_join(sorted(triggers))
        else:
            info = "the requested packages"

        msg = "Cannot install {} because these package versions " \
            "have conflicting dependencies.".format(info)
        logger.critical(msg)
        msg = "\nThe conflict is caused by:"
        for req, parent in e.causes:
            msg = msg + "\n    "
            if parent:
                msg = msg + "{} {} depends on ".format(
                    parent.name,
                    parent.version
                )
            else:
                msg = msg + "The user requested "
            msg = msg + req.format_for_error()

        msg = msg + "\n\n" + \
            "To fix this you could try to:\n" + \
            "1. loosen the range of package versions you've specified\n" + \
            "2. remove package versions to allow pip attempt to solve " + \
            "the dependency conflict\n"

        logger.info(msg)

        return DistributionNotFound(
            "ResolutionImpossible: for help visit "
            "https://pip.pypa.io/en/latest/user_guide/"
            "#fixing-conflicting-dependencies"
        )
