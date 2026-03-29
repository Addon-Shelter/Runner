# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from PySide6 import QtGui
from FreeCAD import Gui


def getActions ():

    window = Gui.getMainWindow()

    items = window.findChildren(QtGui.QAction)

    actions : dict[ str , QtGui.QAction ]= {}

    for item in items :

        name = item.objectName()

        if not name:
            pass

        if name in actions:
            pass

        actions[ name ] = item

    return actions