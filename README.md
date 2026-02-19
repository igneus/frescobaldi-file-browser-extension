# Frescobaldi: file browser extension

This is an extension for the [Frescobaldi][fresco] editor
providing a panel with file browser.

Initially the panel is empty and offers an `Open Folder` button.
On clicking the button a file selection dialog window allows selecting an arbitrary folder
as base folder. Its contents are displayed in the panel as tree of folders and files.
The base folder is always expanded, all nested folders are initially collapsed.
Clicking a folder toggles its expanded state, double-clicking a file opens it in the editor.

## Installation

1. Open Frescobaldi and go to Edit -> Preferences -> Extensions
2. Set the extensions root directory if not already configured
3. Copy or clone this repository into a subdirectory of the extensions root directory
   (the directory name will be used as the extension identifier)
4. Ensure the extension is enabled in the Extensions preference page
5. Restart Frescobaldi

After restart, the File Browser panel will be available in the Tools -> Extensions menu.

[fresco]: https://github.com/frescobaldi/frescobaldi
