# Terminal Emulators integration
[Shell integration](https://iterm2.com/documentation-escape-codes.html) for Xonsh.

The following terminal emulators are supported
- [iTerm2](https://iterm2.com/documentation-shell-integration.html)
- [kitty](https://sw.kovidgoyal.net/kitty/shell-integration/)

**Note**: If identifying current terminal fails, `iTerm2` hooks are loaded.

PRs welcome on improving the support to more terminal programs :)


## Installation

To install use pip:

``` bash
xpip install xontrib-term-integrations
# or: xpip install -U git+https://github.com/jnoortheen/xontrib-term-integrations
```

**Note**: [This PR](https://github.com/xonsh/xonsh/pull/4629) is needed for this to work. As of today(Mar 3, 2022), it is not released yet. So you have to install xonsh from the github like `pipx install git+https://gitlab.com/xonsh/xonsh/`.

## Usage

``` bash
# this modifies the $PROMPT function. So load it after setting $PROMPT if you have a custom value
xontrib load term_integration
```


## Contributing

Please make sure that you
* Document the purpose of functions and classes.
* When adding a new feature, please mention it in the `README.md`. Use screenshots when applicable.
* [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) style should be used
  for commit messages as it is used to generate changelog.
* Please use [pre-commit](https://pre-commit.com/) to run qa checks. Configure it with

```sh
pre-commit install-hooks
```
