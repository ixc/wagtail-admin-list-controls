"""
webpack_manifest.py - https://github.com/markfinger/python-webpack-manifest

MIT License

Copyright (c) 2015-present, Mark Finger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
import time
from datetime import datetime, timedelta

__version__ = '2.1.1'

MANIFEST_CACHE = {}

BUILDING_STATUS = 'building'
BUILT_STATUS = 'built'
ERRORS_STATUS = 'errors'


def load(path, static_url, debug=False, timeout=60, read_retry=None, static_root=None):
    # Enable failed reads to be retried after a delay of 1 second
    if debug and read_retry is None:
        read_retry = 1

    if debug or path not in MANIFEST_CACHE:
        manifest = build(path, static_url, debug, timeout, read_retry, static_root)

        if not debug:
            MANIFEST_CACHE[path] = manifest

        return manifest

    return MANIFEST_CACHE[path]


def build(path, static_url, debug, timeout, read_retry, static_root):
    data = read(path, read_retry)
    status = data.get('status', None)

    if debug:
        # Lock up the process and wait for webpack to finish building
        max_timeout = datetime.utcnow() + timedelta(seconds=timeout)
        while status == BUILDING_STATUS:
            time.sleep(0.1)
            if datetime.utcnow() > max_timeout:
                raise WebpackManifestBuildingStatusTimeout(
                    'Timed out reading the webpack manifest at "{}"'.format(path)
                )
            data = read(path, read_retry)
            status = data.get('status', None)

    if status == ERRORS_STATUS:
        raise WebpackError(
            'Webpack errors: \n\n{}'.format(
                '\n\n'.join(data['errors'])
            )
        )

    if status != BUILT_STATUS:
        raise WebpackManifestStatusError('Unknown webpack manifest status: "{}"'.format(status))

    return WebpackManifest(path, data, static_url, static_root)


class WebpackManifest(object):
    def __init__(self, path, data, static_url, static_root=None):
        self._path = path
        self._data = data
        self._files = data['files']
        self._static_url = static_url
        self._static_root = static_root
        self._manifest_entries = {}

    def __getattr__(self, item):
        if item in self._manifest_entries:
            return self._manifest_entries[item]

        if item in self._files:
            manifest_entry = WebpackManifestEntry(self._files[item], self._static_url, self._static_root)
            self._manifest_entries[item] = manifest_entry
            return manifest_entry

        raise WebpackErrorUnknownEntryError('Unknown entry "%s" in manifest "%s"' % (item, self._path))


class WebpackManifestTypeEntry(object):
    def __init__(self, manifest, static_url, static_root=None):
        self.manifest = manifest
        self.static_url = static_url
        self.static_root = static_root

        self.rel_urls = []
        self.output = ''
        self._content = None
        if self.static_root:
            self.paths = []

    def add_file(self, rel_path):
        rel_url = '/'.join(rel_path.split(os.path.sep))
        self.rel_urls.append(rel_url)
        self.output += self.template.format(self.static_url + rel_url)
        if self.static_root:
            self.paths.append(os.path.join(self.static_root, rel_path))

    def __str__(self):
        return self.output

    @property
    def content(self):
        if self._content is None:
            if not self.static_root:
                raise WebpackManifestConfigError("Provide static_root to access webpack entry content.")

            buffer = []
            for path in self.paths:
                with open(path, 'r') as content_file:
                    buffer.append(content_file.read())
            self._content = '\n'.join(buffer)
        return self._content

    @property
    def inline(self):
        content = self.content
        return self.inline_template.format(content) if content else ''


class WebpackManifestJsEntry(WebpackManifestTypeEntry):
    template = '<script src="{}"></script>'
    inline_template = '<script>{}</script>'


class WebpackManifestCssEntry(WebpackManifestTypeEntry):
    template = '<link rel="stylesheet" href="{}">'
    inline_template = '<style>{}</style>'


class WebpackManifestEntry(object):
    supported_extensions = {
        'js': WebpackManifestJsEntry,
        'css': WebpackManifestCssEntry,
    }

    def __init__(self, rel_paths, static_url, static_root=None):
        # Frameworks tend to be inconsistent about what they
        # allow with regards to static urls
        if not static_url.endswith('/'):
            static_url += '/'

        self.rel_paths = rel_paths
        self.static_url = static_url
        self.static_root = static_root

        for ext, ext_class in self.supported_extensions.items():
            setattr(self, ext, ext_class(self, static_url, static_root))

        # Build strings of elements that can be dumped into a template
        for rel_path in rel_paths:
            name, ext = os.path.splitext(rel_path)
            ext = ext.lstrip('.').lower()
            if ext in self.supported_extensions:
                getattr(self, ext).add_file(rel_path)

    # Backwards compatibility accessors

    @property
    def rel_js(self):
        return self.js.rel_urls

    @property
    def rel_css(self):
        return self.css.rel_urls


def read(path, read_retry):
    if not os.path.isfile(path):
        raise WebpackManifestFileError('Path "{}" is not a file or does not exist'.format(path))

    if not os.path.isabs(path):
        raise WebpackManifestFileError('Path "{}" is not an absolute path to a file'.format(path))

    with open(path, 'r') as manifest_file:
        content = manifest_file.read()

    # In certain conditions, the file's contents evaluate to an empty string, so
    # we provide a hook to perform a single retry after a delay.
    # While it's a difficult bug to pin down it can happen most commonly during
    # periods of high cpu-load, so the suspicion is that it's down to race conditions
    # that are a combination of delays in the OS writing buffers and the fact that we
    # are handling two competing processes
    try:
        return json.loads(content)
    except ValueError:
        if not read_retry:
            raise

        time.sleep(read_retry)
        return read(path, 0)


class WebpackManifestFileError(Exception):
    pass


class WebpackError(Exception):
    pass


class WebpackManifestStatusError(Exception):
    pass


class WebpackManifestBuildingStatusTimeout(Exception):
    pass


class WebpackErrorUnknownEntryError(Exception):
    pass


class WebpackManifestConfigError(Exception):
    pass
