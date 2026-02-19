# This file is part of the Frescobaldi Extensions project,
# https://github.com/frescobaldi-extensions
#
# Copyright (c) 2024 by Claude Code
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
File Browser extension - Tool panel widget
"""

import os

from PyQt6.QtCore import Qt, QDir, QUrl
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QTreeView,
    QWidget,
    QStackedWidget,
    QMenu,
)

from extensions.widget import ExtensionWidget


# File extensions supported by Frescobaldi
SUPPORTED_EXTENSIONS = [
    "*.ly", "*.lyi", "*.ily",           # LilyPond
    "*.tex", "*.lytex", "*.latex",      # LaTeX
    "*.docbook", "*.lyxml",             # DocBook
    "*.html", "*.xml",                  # HTML
    "*.itely", "*.tely", "*.texi", "*.texinfo",  # Texinfo
    "*.scm",                            # Scheme
]


class Widget(ExtensionWidget):
    """The Tool Panel widget with file browser functionality."""

    def __init__(self, panel):
        super().__init__(panel)

        self._root_folder = None

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Stacked widget to switch between empty state and file browser
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Page 0: Empty state with "Open Folder" button
        self.empty_page = QWidget()
        empty_layout = QVBoxLayout()
        empty_layout.addStretch()
        self.open_folder_btn = QPushButton()
        self.open_folder_btn.clicked.connect(self.open_folder)
        empty_layout.addWidget(self.open_folder_btn)
        empty_layout.addStretch()
        self.empty_page.setLayout(empty_layout)
        self.stack.addWidget(self.empty_page)

        # Page 1: File browser tree view
        self.browser_page = QWidget()
        browser_layout = QVBoxLayout()
        browser_layout.setContentsMargins(0, 0, 0, 0)

        # Button to change folder (at the top of the browser view)
        self.change_folder_btn = QPushButton()
        self.change_folder_btn.clicked.connect(self.open_folder)
        browser_layout.addWidget(self.change_folder_btn)

        # File system model and tree view
        self.model = QFileSystemModel()
        self.model.setRootPath("")

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        # Hide all columns except Name
        self.tree.setHeaderHidden(True)
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)
        # Double-click to open files
        self.tree.doubleClicked.connect(self.on_double_click)
        # Single click to toggle folder expansion
        self.tree.clicked.connect(self.on_click)
        # Context menu
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)

        browser_layout.addWidget(self.tree)
        self.browser_page.setLayout(browser_layout)
        self.stack.addWidget(self.browser_page)

        # Start with empty page
        self.stack.setCurrentIndex(0)

        # Apply file filter based on settings
        self.apply_file_filter()

        # Connect to document changes to highlight current file
        self.mainwindow().currentDocumentChanged.connect(self.on_document_changed)

        self.translateUI()

    def translateUI(self):
        self.open_folder_btn.setText(_("Open Folder"))
        self.change_folder_btn.setText(_("Open Folder"))

    def apply_file_filter(self):
        """Apply file name filters based on the 'show_all_files' setting."""
        show_all = self.settings().get('show_all_files')
        if show_all:
            self.model.setNameFilters([])
            self.model.setNameFilterDisables(False)
        else:
            self.model.setNameFilters(SUPPORTED_EXTENSIONS)
            self.model.setNameFilterDisables(False)

    def open_folder(self):
        """Show folder selection dialog and set it as the base folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            _("Select Folder"),
            QDir.homePath(),
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.set_root_folder(folder)

    def set_root_folder(self, folder):
        """Set the given folder as the root of the file browser."""
        self._root_folder = folder
        root_index = self.model.setRootPath(folder)
        self.tree.setRootIndex(root_index)
        # Expand the root folder
        self.tree.expand(root_index)
        # Switch to browser view
        self.stack.setCurrentIndex(1)
        # Update button text to show current folder
        self.change_folder_btn.setText(os.path.basename(folder) or folder)
        # Highlight current document if within this folder
        self.highlight_current_document()

    def on_click(self, index):
        """Handle single click - toggle folder expansion."""
        if self.model.isDir(index):
            if self.tree.isExpanded(index):
                self.tree.collapse(index)
            else:
                self.tree.expand(index)

    def on_double_click(self, index):
        """Handle double-click - open files in the editor."""
        if not self.model.isDir(index):
            file_path = self.model.filePath(index)
            url = QUrl.fromLocalFile(file_path)
            self.mainwindow().openUrl(url)

    def show_context_menu(self, position):
        """Show context menu with options."""
        menu = QMenu(self)

        # "Show All Files" toggle action
        show_all_action = QAction(_("Show All Files"), self)
        show_all_action.setCheckable(True)
        show_all_action.setChecked(self.settings().get('show_all_files'))
        show_all_action.triggered.connect(self.toggle_show_all_files)
        menu.addAction(show_all_action)

        menu.exec(self.tree.viewport().mapToGlobal(position))

    def toggle_show_all_files(self, checked):
        """Toggle the 'show_all_files' setting."""
        self.settings().set('show_all_files', checked)
        self.apply_file_filter()

    def on_document_changed(self, new_doc, old_doc):
        """Handle document change - highlight the current file in the tree."""
        self.highlight_current_document()

    def highlight_current_document(self):
        """Highlight the currently open document in the tree view."""
        if not self._root_folder:
            return

        doc = self.current_document()
        if not doc:
            return

        url = doc.url()
        if url.isEmpty():
            return

        file_path = url.toLocalFile()
        if not file_path:
            return

        # Check if the file is within the current root folder
        if not file_path.startswith(self._root_folder + os.sep) and file_path != self._root_folder:
            return

        # Get the index for this file path
        index = self.model.index(file_path)
        if index.isValid():
            # Expand parent folders to make the file visible
            parent = index.parent()
            while parent.isValid() and parent != self.tree.rootIndex():
                self.tree.expand(parent)
                parent = parent.parent()
            # Select and scroll to the file
            self.tree.setCurrentIndex(index)
            self.tree.scrollTo(index)
