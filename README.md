# Frescobaldi: file browser extension

This is an extension for the [Frescobaldi][fresco] editor
providing a panel with file browser.

Initially the panel is empty and offers an `Open Folder` button.
On clicking the button a file selection dialog window allows selecting an arbitrary folder
as base folder. Its contents are displayed in the panel as tree of folders and files.
The base folder is always expanded, all nested folders are initially collapsed.
Clicking a folder toggles its expanded state, double-clicking a file opens it in the editor.

[fresco]: https://github.com/frescobaldi/frescobaldi
