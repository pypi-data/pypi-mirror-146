# -*- coding: utf-8 -*-
"""upload_docs

Implements a Distutils 'upload_docs' subcommand (upload documentation to
PyPI's pythonhosted.org).
"""

from base64 import standard_b64encode
from distutils import log
from distutils.errors import DistutilsOptionError
import os
import socket
import zipfile
import tempfile
import shutil
import itertools
import functools

if "__PEX_UNVENDORED__" in __import__("os").environ:
  from setuptools.extern import six  # vendor:skip
else:
  from pex.third_party.setuptools.extern import six

if "__PEX_UNVENDORED__" in __import__("os").environ:
  from setuptools.extern.six.moves import http_client, urllib  # vendor:skip
else:
  from pex.third_party.setuptools.extern.six.moves import http_client, urllib


if "__PEX_UNVENDORED__" in __import__("os").environ:
  from pkg_resources import iter_entry_points  # vendor:skip
else:
  from pex.third_party.pkg_resources import iter_entry_points

from .upload import upload


def _encode(s):
    errors = 'surrogateescape' if six.PY3 else 'strict'
    return s.encode('utf-8', errors)


class upload_docs(upload):
    # override the default repository as upload_docs isn't
    # supported by Warehouse (and won't be).
    DEFAULT_REPOSITORY = 'https://pypi.python.org/pypi/'

    description = 'Upload documentation to PyPI'

    user_options = [
        ('repository=', 'r',
         "url of repository [default: %s]" % upload.DEFAULT_REPOSITORY),
        ('show-response', None,
         'display full response text from server'),
        ('upload-dir=', None, 'directory to upload'),
    ]
    boolean_options = upload.boolean_options

    def has_sphinx(self):
        if self.upload_dir is None:
            for ep in iter_entry_points('distutils.commands', 'build_sphinx'):
                return True

    sub_commands = [('build_sphinx', has_sphinx)]

    def initialize_options(self):
        upload.initialize_options(self)
        self.upload_dir = None
        self.target_dir = None

    def finalize_options(self):
        upload.finalize_options(self)
        if self.upload_dir is None:
            if self.has_sphinx():
                build_sphinx = self.get_finalized_command('build_sphinx')
                self.target_dir = build_sphinx.builder_target_dir
            else:
                build = self.get_finalized_command('build')
                self.target_dir = os.path.join(build.build_base, 'docs')
        else:
            self.ensure_dirname('upload_dir')
            self.target_dir = self.upload_dir
        if 'pypi.python.org' in self.repository:
            log.warn("Upload_docs command is deprecated. Use RTD instead.")
        self.announce('Using upload directory %s' % self.target_dir)

    def create_zipfile(self, filename):
        zip_file = zipfile.ZipFile(filename, "w")
        try:
            self.mkpath(self.target_dir)  # just in case
            for root, dirs, files in os.walk(self.target_dir):
                if root == self.target_dir and not files:
                    tmpl = "no files found in upload directory '%s'"
                    raise DistutilsOptionError(tmpl % self.target_dir)
                for name in files:
                    full = os.path.join(root, name)
                    relative = root[len(self.target_dir):].lstrip(os.path.sep)
                    dest = os.path.join(relative, name)
                    zip_file.write(full, dest)
        finally:
            zip_file.close()

    def run(self):
        # Run sub commands
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)

        tmp_dir = tempfile.mkdtemp()
        name = self.distribution.metadata.get_name()
        zip_file = os.path.join(tmp_dir, "%s.zip" % name)
        try:
            self.create_zipfile(zip_file)
            self.upload_file(zip_file)
        finally:
            shutil.rmtree(tmp_dir)

    @staticmethod
    def _build_part(item, sep_boundary):
        key, values = item
        title = '\nContent-Disposition: form-data; name="%s"' % key
        # handle multiple entries for the same name
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if isinstance(value, tuple):
                title += '; filename="%s"' % value[0]
                value = value[1]
            else:
                value = _encode(value)
            yield sep_boundary
            yield _encode(title)
            yield b"\n\n"
            yield value
            if value and value[-1:] == b'\r':
                yield b'\n'  # write an extra newline (lurve Macs)

    @classmethod
    def _build_multipart(cls, data):
        """
        Build up the MIME payload for the POST data
        """
        boundary = b'--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'
        sep_boundary = b'\n--' + boundary
        end_boundary = sep_boundary + b'--'
        end_items = end_boundary, b"\n",
        builder = functools.partial(
            cls._build_part,
            sep_boundary=sep_boundary,
        )
        part_groups = map(builder, data.items())
        parts = itertools.chain.from_iterable(part_groups)
        body_items = itertools.chain(parts, end_items)
        content_type = 'multipart/form-data; boundary=%s' % boundary.decode('ascii')
        return b''.join(body_items), content_type

    def upload_file(self, filename):
        with open(filename, 'rb') as f:
            content = f.read()
        meta = self.distribution.metadata
        data = {
            ':action': 'doc_upload',
            'name': meta.get_name(),
            'content': (os.path.basename(filename), content),
        }
        # set up the authentication
        credentials = _encode(self.username + ':' + self.password)
        credentials = standard_b64encode(credentials)
        if six.PY3:
            credentials = credentials.decode('ascii')
        auth = "Basic " + credentials

        body, ct = self._build_multipart(data)

        msg = "Submitting documentation to %s" % (self.repository)
        self.announce(msg, log.INFO)

        # build the Request
        # We can't use urllib2 since we need to send the Basic
        # auth right with the first request
        schema, netloc, url, params, query, fragments = \
            urllib.parse.urlparse(self.repository)
        assert not params and not query and not fragments
        if schema == 'http':
            conn = http_client.HTTPConnection(netloc)
        elif schema == 'https':
            conn = http_client.HTTPSConnection(netloc)
        else:
            raise AssertionError("unsupported schema " + schema)

        data = ''
        try:
            conn.connect()
            conn.putrequest("POST", url)
            content_type = ct
            conn.putheader('Content-type', content_type)
            conn.putheader('Content-length', str(len(body)))
            conn.putheader('Authorization', auth)
            conn.endheaders()
            conn.send(body)
        except socket.error as e:
            self.announce(str(e), log.ERROR)
            return

        r = conn.getresponse()
        if r.status == 200:
            msg = 'Server response (%s): %s' % (r.status, r.reason)
            self.announce(msg, log.INFO)
        elif r.status == 301:
            location = r.getheader('Location')
            if location is None:
                location = 'https://pythonhosted.org/%s/' % meta.get_name()
            msg = 'Upload successful. Visit %s' % location
            self.announce(msg, log.INFO)
        else:
            msg = 'Upload failed (%s): %s' % (r.status, r.reason)
            self.announce(msg, log.ERROR)
        if self.show_response:
            print('-' * 75, r.read(), '-' * 75)
