Sublimacs
=========

A plugin for Sublime Text 2 to make Sublime as good as Emacs for day-to-day text editing operations.

The goal is to reproduce the best features of Emacs and follow Emacs key bindings as much as possible, while providing the best possible integration with other Sublime and platform functions (like the system pasteboard/clipboard).

Status: early development.

Features:

* kill ring

Planned:

* mark history
* make all clipboard commands use the kill ring and mark history
* better mark support when pasting
* more Emacs hot keys

Contribute your favourite Emacs features, it's dead-easy! (See below for a contributor's guide.)


Installation
------------

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone http://github.com/andreyvit/Sublimacs


Key bindings
------------

The following keys are modified by this plugin:

    C-space           set mark (currently a Sublime command, mark history coming)
    M-/               auto complete

    C-w               kill
    M-w               save to kill ring
    C-k               kill to end of line

    C-y               yank
    M-y               yank previous
    M-S-y             yank next (there is no such command in Emacs, but hey)


Contributor's Guide
-------------------

So how do you start writing Sublime Text 2 plugins? Turns out, it is very easy. A few pointers:

* use Tools > New Plugin (or see Sublimacs.py); there are two key imports: `sublime` and `sublime_plugin`
* `sublime` is fully documented in [the API reference here](http://www.sublimetext.com/docs/2/api_reference.html)
* `sublime_plugin` is also documented in the API reference, but you'd better read its source code which is included with Sublime; on my system it is in `/Applications/Sublime Text 2.app/Contents/MacOS/sublime_plugin.py`
* read implementations of many existing Sublime commands in `~/Library/Application Support/Sublime Text 2/Packages/Default`
* finally, see the implementations of Sublimacs commands in `Sublimacs.py`
* Sublime automatically loads and reloads any files inside its packages directory, all key bindings, settings and listeners are applied live
* open console window (View > Show Console) to interact with the built-in Python interpreter
* in the console, use `view.run_command('foo_bar')` to run `FooBarCommand` (or generally use `view`, `window`, `sublime` objects to explore the API)
* add custom key bindings for your commands in `Default (OSX).sublime-keymap`

That should get you started with anything you might want to implement.

There is [an outdated Emacs kill ring implementation here](http://sublime-text-community-packages.googlecode.com/svn/pages/EmacsKillRing.html), but it does not work on a recent version of Sublime (at least on OS X). Still might be a good read.
