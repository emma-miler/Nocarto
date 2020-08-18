from PyQt5 import QtWidgets, QtGui, QtCore

class QNodeDetailDialog(QtWidgets.QDialog):
    def __init__(self, node, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setMinimumSize(300, 500)

        self.nodeDeltaOld = {} # Holds the old values of changed data
        self.nodeDeltaNew = {} # Holds the new values of changed data

        self.node = node

        self.apply = False # Whether or not to apply data when closing. To be handled by invoker

        # Add a top text to the dialog
        self.topText = QtWidgets.QLabel("Edit Node")
        self.topText.setStyleSheet("font-size: 12pt")
        self.topText.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.topText)

        self.nameBox = QtWidgets.QWidget()
        self.nameLayout = QtWidgets.QHBoxLayout()
        self.nameBox.setLayout(self.nameLayout)
        self.nameLabel = QtWidgets.QLabel("Name:")
        self.nameLayout.addWidget(self.nameLabel)
        self.nameInput = QtWidgets.QLineEdit(node.name)
        self.nameInput.textEdited.connect(self.nameChanged)
        self.nameLayout.addWidget(self.nameInput)
        self.layout.addWidget(self.nameBox)


        self.colorBox = QtWidgets.QWidget()
        self.colorLayout = QtWidgets.QHBoxLayout()
        self.colorBox.setLayout(self.colorLayout)
        self.colorLabel = QtWidgets.QLabel("Color:")
        self.colorLayout.addWidget(self.colorLabel)
        self.colorInput = QtWidgets.QPushButton()
        if "color" in node.data:
            self.colorInput.setStyleSheet("background-color: " + node.data["color"])
        else:
            self.colorInput.setStyleSheet("background-color: " + "black")
            self.colorInput.setText("None")
        self.colorInput.clicked.connect(self.openColorDialog)
        self.colorLayout.addWidget(self.colorInput)
        self.layout.addWidget(self.colorBox)

        self.textLabel = QtWidgets.QLabel("Additional text:")
        self.layout.addWidget(self.textLabel)
        self.textInput = QtWidgets.QTextEdit()
        if "text" in node.data:
            self.textInput.setText(node.data["text"])
        self.textInput.textChanged.connect(self.textChanged)
        self.layout.addWidget(self.textInput)

        self.dataLabel = QtWidgets.QLabel("Other data:")
        self.layout.addWidget(self.dataLabel)

        self.dataTable = QtWidgets.QTableView()
        self.layout.addWidget(self.dataTable)

        self.model = QtGui.QStandardItemModel()

        for item in node.data.keys():
            if item == "color" or item == "text": # These are already handled as seperate widgets
                continue
            name = QtGui.QStandardItem(str(item))
            name.setFlags(QtCore.Qt.ItemIsEnabled)
            shortcut = QtGui.QStandardItem(str(node.data[item]))
            shortcut.setFlags(QtCore.Qt.ItemIsEnabled)
            self.model.invisibleRootItem().appendRow( [name, shortcut] )

        self.dataTable.horizontalHeader().hide()
        self.dataTable.verticalHeader().hide()

        self.dataTable.horizontalHeader().setStretchLastSection(True)
        self.dataTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.dataTable.setModel(self.model)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.buttons()[1].clicked.connect(self.closeApply)
        self.buttonBox.buttons()[0].clicked.connect(self.close)
        self.layout.addWidget(self.buttonBox)

    def openColorDialog(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.colorInput.setText("")
            self.colorInput.setStyleSheet(f"background-color: {color.name()}")
            print(color.name())
            if "color" in self.node.data:
                oldColor = self.node.data["color"]
            else:
                oldColor = None
                
            if "data" in self.nodeDeltaOld:
                self.nodeDeltaOld["data"]["color"] = oldColor
                self.nodeDeltaNew["data"]["color"] = color.name()
            else:
                self.nodeDeltaOld["data"] = {"color": oldColor}
                self.nodeDeltaNew["data"] = {"color": color.name()}

    def nameChanged(self, event):
        self.nodeDeltaNew["name"] = event
        if "name" not in self.nodeDeltaOld:
            self.nodeDeltaOld["name"] = self.node.name
    
    def textChanged(self):
        event = str(self.textInput.toPlainText())
        if "data" in self.nodeDeltaNew:
            self.nodeDeltaNew["data"]["text"] = event
            if not "text" in self.nodeDeltaOld:
                if "text" in self.node.data:
                    self.nodeDeltaOld["data"] = {"text": self.node.data["text"]}
                else:
                    self.nodeDeltaOld["data"] = {"text": ""}
        else:
            if "text" in self.node.data:
                self.nodeDeltaOld["data"] = {"text": self.node.data["text"]}
            else:
                self.nodeDeltaOld["data"] = {"text": ""}
            self.nodeDeltaNew["data"] = {"text": event}

    def closeApply(self):
        self.apply = True
        self.close()