Sublimacs
=========

A plugin for Sublime Text 2 to make Sublime as good as Emacs for day-to-day text editing operations.

The goal is to reproduce the best features of Emacs and follow Emacs key bindings as much as possible, while providing the best possible integration with other Sublime and platform functions (like the system pasteboard/clipboard).

Status: early development.

Features:
* kill ring


Installation
------------

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone http://github.com/andreyvit/sublimacs


Key bindings
------------

The following keys are modified by this plugin:

    C-space           set mark (currently a Sublime command, mark history coming)
    M-/               auto complete

    C-w               kill
    M-w               save to kill ring

    C-y               yank
    M-y               yank previous
    M-S-y             yank next (there is no such command in Emacs, but hey)
