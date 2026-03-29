# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from PySide6 import QtWidgets , QtCore , QtGui
from FreeCAD import Gui

from .Shortcut import registerShortcut
from .Actions import getActions
from .Item import toItem


def registerDock ():

    window = Gui.getMainWindow()

    class Search ( QtWidgets.QLineEdit ):

        def __init__ ( self , parent = None ):
            super(Search,self).__init__(parent)

        def focusInEvent ( self , event : QtGui.QFocusEvent ):
            if event.reason() != QtCore.Qt.FocusReason.PopupFocusReason:
                updateResults()

        def keyPressEvent ( self , event : QtGui.QKeyEvent ):

            if event.key() == QtCore.Qt.Key.Key_Down:
                search.clear()
                completer.setCompletionPrefix('')
                completer.complete()
                return

            QtWidgets.QLineEdit.keyPressEvent(self,event)
            index = results.index(0,0)
            popup = completer.popup()

            if popup:
                popup.setCurrentIndex(index)

    completer = QtWidgets.QCompleter()
    completer.setMaxVisibleItems(16)
    completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
    completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
    completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)

    search = Search()
    search.setCompleter(completer)

    results = QtGui.QStandardItemModel()
    completer.setModel(results)

    dock = QtWidgets.QDockWidget()
    dock.setWindowTitle('Runner')
    dock.setObjectName('Runner')
    dock.setWidget(search)

    window.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,dock)


    def updateResults ():

        actions = getActions()

        results.clear()
        results.setRowCount( len(actions) )
        results.setColumnCount(1)

        row = 0

        for name in actions:

            action = actions[ name ]

            item = toItem(action)

            results.setItem(row,0,item)
            row += 1


    def onComplete (
        index : QtCore.QModelIndex
    ):

        completion = completer.completionModel()

        if not isinstance(completion,QtCore.QAbstractProxyModel):
            return

        index = completion.mapToSource(index)

        item = results.itemFromIndex(index)

        name : str = item.data(QtCore.Qt.ItemDataRole.UserRole)

        actions = getActions()

        if not name in actions :
            return

        actions[ name ].trigger()

        search.clear()
        search.clearFocus()
        search.setFocus()

    completer.activated[ QtCore.QModelIndex ].connect(onComplete) # type: ignore

    registerShortcut(search.setFocus)
