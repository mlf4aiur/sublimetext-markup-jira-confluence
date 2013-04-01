Post markup to Jira Confluence
==============================

This is a simple plugin for sublime text to POST markup to Jira Confluence.

Support markup language:

* markdown depend on [python-markdown2][0]
* reStructuredText depend on docutils

Installation
------------

**Use sublime package manager**

 - you should use [sublime package manager][1]
 - use `cmd+shift+P` then `Package Control: Install Package`
 - look for `Jira Confluence` and install it.

**Manually**

At the moment Git is required to install the plugin.  You will need
to clone the repository in your Sublime Text "Packages" directory:

`git clone git@github.com:mlf4aiur/sublimetext-markup-jira-confluence.git`

The "Packages" directory is located at:

* OS X: `~/Library/Application Support/Sublime Text 2/Packages/`
* Linux: `~/.Sublime Text 2/Packages/`
* Windows: `%APPDATA%/Sublime Text 2/Packages/`


Usage
-----

Use Command Palette to run it, use `cmd+shift+P` then `Post page to Jira Confluence` to post local page to remote.

[0]: https://github.com/trentm/python-markdown2
[1]: http://wbond.net/sublime_packages/package_control
