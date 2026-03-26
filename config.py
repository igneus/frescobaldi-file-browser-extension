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
File Browser extension - Configuration widget
"""

from PyQt6.QtWidgets import (
    QCheckBox,
    QVBoxLayout,
    QWidget,
)


class Config(QWidget):
    """Configuration widget, shown in the Preferences page."""

    def __init__(self, group):
        super().__init__(group)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Checkbox for "Show All Files" option
        self.show_all_files_checkbox = QCheckBox(toggled=group.changed)
        layout.addWidget(self.show_all_files_checkbox)

        layout.addStretch()

        self.translateUI()

    def translateUI(self):
        self.show_all_files_checkbox.setText(
            _("Show all files (not just Frescobaldi-supported types)"))

    def load_settings(self):
        self.show_all_files_checkbox.setChecked(
            self.settings().get('show_all_files'))

    def save_settings(self):
        self.settings().set(
            'show_all_files', self.show_all_files_checkbox.isChecked())
