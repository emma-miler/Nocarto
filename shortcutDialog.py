from PyQt5 import QtGui, QtWidgets, QtCore

class ShortcutDialog(QtWidgets.QDialog):
    def __init__(self, shortcuts, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setMinimumSize(300, 500)

        self.topText = QtWidgets.QLabel("Keyboard shortcuts")
        self.topText.setStyleSheet("font-size: 18pt")
        self.topText.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.topText)

        self.shortcuts = QtWidgets.QTableView()
        self.layout.addWidget(self.shortcuts)

        self.model = QtGui.QStandardItemModel()

        for shortcut in shortcuts:
            name = QtGui.QStandardItem(shortcut.text())
            name.setFlags(QtCore.Qt.ItemIsEnabled)
            shortcut = QtGui.QStandardItem(shortcut.shortcut().toString())
            shortcut.setFlags(QtCore.Qt.ItemIsEnabled)
            self.model.invisibleRootItem().appendRow( [name, shortcut] )

        self.shortcuts.horizontalHeader().hide()
        self.shortcuts.verticalHeader().hide()

        self.shortcuts.horizontalHeader().setStretchLastSection(True)
        self.shortcuts.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.shortcuts.setModel(self.model)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.buttons()[0].clicked.connect(self.close)
        self.layout.addWidget(self.buttonBox)