# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from PySide6 import QtWidgets , QtCore , QtGui
from FreeCAD import Gui


def singleInstance():
    """
    Only have one instance of Launcher running.
    """

    mw = Gui.getMainWindow()

    if mw:
        for i in mw.findChildren(QtWidgets.QDockWidget):
            if i.objectName() == "Launcher":
                i.deleteLater()
            else:
                pass
    else:
        pass

singleInstance()


def dockWidget():
    """
    Launcher widget for FreeCAD
    """

    mw = Gui.getMainWindow()

    icon = """<svg xmlns="http://www.w3.org/2000/svg" height="64" width="64">
              <rect height="64" width="64" fill="none" />
              </svg>"""

    iconPixmap = QtGui.QPixmap()
    iconPixmap.loadFromData(QtCore.QByteArray(icon.encode()))

    class LauncherEdit(QtWidgets.QLineEdit):
        """
        Define completer show/hide behavior.
        """
        def __init__(self, parent=None):
            super(LauncherEdit, self).__init__(parent)

        def focusInEvent(self, event : QtGui.QFocusEvent ):
            """
            Prevent updating model data after closing completer.
            """
            if event.reason() == QtCore.Qt.FocusReason.PopupFocusReason:
                pass
            else:
                modelData()

        def keyPressEvent(self, event : QtGui.QKeyEvent):
            """
            Show completer after down key is pressed.
            """
            if event.key() == QtCore.Qt.Key.Key_Down:
                edit.clear()
                completer.setCompletionPrefix("")
                completer.complete()
            else:
                QtWidgets.QLineEdit.keyPressEvent(self, event)
                index = model.index(0, 0)
                popup = completer.popup()

                if popup:
                    popup.setCurrentIndex(index)

    completer = QtWidgets.QCompleter()
    completer.setMaxVisibleItems(16)
    completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
    try:
        # Qt 5.2 and up.
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
    except AttributeError:
        pass

    edit = LauncherEdit()
    edit.setCompleter(completer)

    model = QtGui.QStandardItemModel()
    completer.setModel(model)

    widget = QtWidgets.QDockWidget()
    widget.setWindowTitle("Launcher")
    widget.setObjectName("Launcher")
    widget.setWidget(edit)

    if mw:
        mw.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, widget)
    else:
        pass

    def modelData():
        """
        Fill the model with model items.
        """
        actions = {}
        duplicates = []

        for i in mw.findChildren(QtGui.QAction):
            if i.objectName():
                if i.objectName() in actions:
                    if i.objectName() not in duplicates:
                        duplicates.append(i.objectName())
                    else:
                        pass
                else:
                    actions[i.objectName()] = i
            else:
                pass

        for d in duplicates:
            del actions[d]

        rows = len(actions)

        model.clear()
        model.setRowCount(rows)
        model.setColumnCount(1)

        row = 0

        for i in actions:

            item = QtGui.QStandardItem()
            item.setText((actions[i].text()).replace("&", ""))
            if actions[i].icon():
                item.setIcon(actions[i].icon())
            else:
                item.setIcon(QtGui.QIcon(QtGui.QIcon(iconPixmap)))
            item.setToolTip(actions[i].toolTip())
            item.setEnabled(actions[i].isEnabled())
            item.setData(actions[i].objectName(),QtCore.Qt.ItemDataRole.UserRole)

            model.setItem(row, 0, item)
            row += 1

    def onCompleter(modelIndex):
        """
        When command is selected and triggered run it and update model data.
        """
        actions = {}

        for i in mw.findChildren(QtGui.QAction):
            actions[i.objectName()] = i

        item_model = completer.completionModel()

        if isinstance(item_model,QtCore.QAbstractProxyModel):

            index = item_model.mapToSource(modelIndex)

            item = model.itemFromIndex(index)
            data = item.data(QtCore.Qt.ItemDataRole.UserRole)

            if data in actions:
                actions[data].trigger()
            else:
                pass

            edit.clear()
            edit.clearFocus()
            edit.setFocus()

    completer.activated.connect(onCompleter)

    action = QtGui.QAction(mw)
    mw.addAction(action)
    action.setText("Launcher focus")
    action.setObjectName("SetLauncherFocus")
    action.setShortcut(QtGui.QKeySequence("Ctrl+Shift+Q"))

    action.triggered.connect(edit.setFocus)


dockWidget()
