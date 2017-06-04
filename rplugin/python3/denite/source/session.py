# ============================================================================
# FILE: session.py
# AUTHOR: Rafael Bodill <justRafi at gmail.com>
# License: MIT license
# ============================================================================

import os
import time

from denite.util import globruntime
from .base import Base


class Source(Base):
    """ Vim session loader source for Denite.nvim """

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'session'
        self.kind = 'session'
        self.vars = {
            'path': vim.vars.get('session_directory', None),
            'pattern': '*'
        }

    def on_init(self, context):
        if not self.vars.get('path'):
            raise AttributeError('Invalid session directory, please configure')

    def highlight(self):
        self.vim.command(
            'highlight default link {} Special'.format(self.syntax_name))
        self.vim.command(
            'highlight default link deniteSessionTime Comment')

    def define_syntax(self):
        super().define_syntax()
        self.vim.command(
            'syntax match deniteSessionTime /(.\{-})/ '
            'containedin=' + self.syntax_name)

    def gather_candidates(self, context):
        candidates = []
        now = time.time()
        path = os.path.expanduser(self.vars['path'])

        for path in globruntime(path, self.vars['pattern']):
            mtime = os.stat(path).st_mtime
            name = os.path.splitext(os.path.basename(path))[0]
            candidates.append({
                'word': '%s (%s)' % (name, self._time_ago(now, mtime)),
                'action__path': path,
                'source_mtime': mtime,
            })

        return sorted(
            candidates,
            key=lambda x: x['source_mtime'],
            reverse=True)

    def _time_ago(self, now, seconds):
        """ Return relative difference of two timestamps """
        diff = now - seconds
        if diff <= 0:
            return 'just now'
        if diff < 60:
            return str(int(diff)) + ' seconds ago'
        if diff / 60 < 60:
            return str(int(diff/60)) + ' minutes ago'
        if diff / 3.6e+3 < 24:
            return str(int(diff/3.6e+3)) + ' hours ago'
        if diff / 8.64e+4 < 24:
            return str(int(diff/8.64e+4)) + ' days ago'
        if diff / 6.048e+5 < 4.34812:
            return str(int(diff/6.048e+5)) + ' weeks ago'
        if diff / 2.63e+6 < 12:
            return str(int(diff/2.63e+6)) + ' months ago'

        return str(int(diff/3.156e+7)) + 'years ago'
