# ============================================================================
# FILE: session.py
# AUTHOR: Rafael Bodill <justRafi at gmail.com>
# License: MIT license
# ============================================================================

import os

from .openable import Kind as Openable
from denite import util


class Kind(Openable):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'session'
        self.default_action = 'open'

    def action_open(self, context):
        """ Loads first selected session after wiping out all buffers """
        target = context['targets'][0]
        path = target['action__path']

        current = self.vim.eval('v:this_session')
        if current and 'SessionLoad' not in self.vim.vars:
            self.vim.command('mksession! {}'.format(current))

        self.vim.command('noautocmd silent! %bwipeout!')
        self.vim.command('silent! source {}'.format(path))

    def action_preview(self, context):
        """ Opens a session anonymously """
        current_exists = int(self.vim.eval('exists("v:this_session")'))
        if current_exists:
            current = self.vim.eval('v:this_session')
        else:
            current = ""
        self.action_open(context)
        self.vim.command("let v:this_session = '{}'".format(current))

    def action_delete(self, context):
        """ Delete selected session(s) """
        for target in context['targets']:
            file_path = target['action__path']
            if len(file_path) < 2 or not os.path.isfile(file_path):
                continue

            msg = 'Delete session `{}` ? '.format(os.path.basename(file_path))
            if util.input(self.vim, context, msg) not in ['y', 'yes']:
                continue

            self.vim.call('delete', target['action__path'])
            if self.vim.eval('v:this_session') == file_path:
                self.vim.command("let v:this_session = ''")

    def action_save(self, context):
        """ Overwrite the first selected session """
        target = context['targets'][0]
        file_path = target['action__path']
        self.vim.call('delete', file_path)
        self.vim.command("mksession! '{}'".format(file_path))
        self.vim.command("let v:this_session = '{}'".format(file_path))
