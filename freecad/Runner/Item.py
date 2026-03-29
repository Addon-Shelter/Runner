# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from PySide6 import QtCore , QtGui


icon = '''
    <svg xmlns="http://www.w3.org/2000/svg" height="64" width="64">
        <rect height="64" width="64" fill="none" />
    </svg>
'''


def svgToPixmap ( svg : str ):
    icon = QtGui.QPixmap()
    icon.loadFromData(QtCore.QByteArray(svg.encode()))
    return icon


Placeholder = svgToPixmap(icon)


def toItem (
    action : QtGui.QAction
):

    text = action.text().replace('&','')
    icon = action.icon() or Placeholder

    item = QtGui.QStandardItem()
    item.setToolTip(action.toolTip())
    item.setEnabled(action.isEnabled())
    item.setData(action.objectName(),QtCore.Qt.ItemDataRole.UserRole)
    item.setText(text)
    item.setIcon(icon)

    return item
