# denite-session

Browse and open sessions with this Denite source.

## Features

- Load, delete, and save sessions
- Custom global path for sessions

## Installation

Use your favorite plugin manager, mine is [dein.vim].

### Requirements

- Vim or Neovim
- [denite.nvim]
- Python 3.4 or later

## Usage

```viml
:Denite session
```

### Configuration

The default path for sessions can be set with `g:session_directory`

Or, you can set the path option via Denite:

```viml
call denite#custom#var('session', 'path', '~/.vim-sessions')
```

## Credits & Contribution

This plugin is maintained by Rafael Bodill.

Pull requests are welcome.

[denite.nvim]: https://github.com/Shougo/denite.nvim
[dein.vim]: https://github.com/Shougo/dein.vim
