from PyQt5 import QtGui, QtWidgets, QtCore

class HotkeyDialog(QtWidgets.QDialog):
    def __init__(self, hotkeys, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setMinimumSize(300, 500)

        self.topText = QtWidgets.QLabel("Keyboard shortcuts")
        self.topText.setStyleSheet("font-size: 18pt")
        self.topText.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.topText)

        self.hotkeys = QtWidgets.QTableView()
        self.layout.addWidget(self.hotkeys)

        self.model = QtGui.QStandardItemModel()

        for x in range(0, 10):
            self.model.invisibleRootItem().appendRow( [
                QtGui.QStandardItem(str(x) + "testaiohasodh"),
                QtGui.QStandardItem(str(x))
            ])

        self.hotkeys.horizontalHeader().hide()
        self.hotkeys.verticalHeader().hide()

        self.hotkeys.horizontalHeader().setStretchLastSection(True)
        self.hotkeys.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.hotkeys.setModel(self.model)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.layout.addWidget(self.buttonBox)