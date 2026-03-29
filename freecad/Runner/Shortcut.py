# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from PySide6 import QtGui
from FreeCAD import Gui
from types import MethodType


def registerShortcut (
    callback : MethodType
):

    window = Gui.getMainWindow()

    action = QtGui.QAction(window)
    action.setObjectName('SetRunnerFocus')
    action.setShortcut(QtGui.QKeySequence('Ctrl+Shift+P'))
    action.setText('Runner focus')

    window.addAction(action)

    action.triggered.connect(callback)
