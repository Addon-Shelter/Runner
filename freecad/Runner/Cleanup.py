# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from PySide6 import QtWidgets
from FreeCAD import Gui


def removeExisting ():

    window = Gui.getMainWindow()

    if not window:
        pass

    docks = window.findChildren(QtWidgets.QDockWidget)

    for dock in docks :
        if dock.objectName() == 'Runner' :
            dock.deleteLater()
