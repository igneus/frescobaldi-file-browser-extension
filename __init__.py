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
File Browser Frescobaldi extension

Provides a panel with a file browser for navigating directories
and opening files in the editor.
"""

from PyQt6.QtCore import Qt
import extensions
from . import config, widget


class Extension(extensions.Extension):
    """
    File Browser extension.

    Provides a tool panel with a file browser that allows:
    - Selecting a base folder via "Open Folder" button
    - Displaying folder contents as a tree
    - Opening files by double-clicking
    """

    _panel_widget_class = widget.Widget
    _panel_dock_area = Qt.DockWidgetArea.LeftDockWidgetArea
    _config_widget_class = config.Config
    _settings_config = {
        'show_all_files': False
    }

    def settings_changed(self, key, old, new):
        """Update the panel when settings change."""
        if key == 'show_all_files':
            panel_widget = self.widget()
            if panel_widget:
                panel_widget.apply_file_filter()
