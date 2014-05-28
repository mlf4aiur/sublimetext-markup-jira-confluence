Markup to Confluence - Sublime Text 2/3
=======================================

A plugin for post markup to Confluence in Sublime 2/3.

Support markup language:

* markdown depend on [python-markdown2][0]
* reStructuredText depend on docutils

Installation
------------

**Use sublime package manager**

 - you should use [sublime package manager][1]
 - use `cmd+shift+p` then `Package Control: Install Package`
 - look for `Jira Confluence` and install it.

**Manually**

At the moment Git is required to install the plugin.  You will need
to clone the repository in your Sublime Text "Packages" directory:

`git clone git@github.com:mlf4aiur/sublimetext-markup-jira-confluence.git "Markup Jira Confluence"`

The "Packages" directory is located at:

* OS X: `~/Library/Application Support/Sublime Text */Packages/`
* Linux: `~/.Sublime Text */Packages/`
* Windows: `%APPDATA%/Sublime Text */Packages/`


Usage
-----

META data must give, and put it on the head of document, use newline to separate META data and content.

Example file: example.md, example.rst.

META data:

* Space
* Parent Title
* Title

Use Command Palette to run it, use `cmd+shift+p` then `Post page to Jira Confluence` to post local page to remote.

BTW
---


[0]: https://github.com/trentm/python-markdown2
[1]: http://wbond.net/sublime_packages/package_control
