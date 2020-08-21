from PyQt5 import QtWidgets, QtGui, QtCore

class QEdgeDetailDialog(QtWidgets.QDialog):
    def __init__(self, edge, parent=None):
        super().__init__(parent=parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setMinimumSize(300, 500)

        self.edgeDeltaOld = {} # Holds the old values of changed data
        self.edgeDeltaNew = {} # Holds the new values of changed data

        self.edge = edge

        self.apply = False # Whether or not to apply data when closing. To be handled by invoker

        # Add a top text to the dialog
        self.topText = QtWidgets.QLabel("Edit Edge")
        self.topText.setStyleSheet("font-size: 12pt")
        self.topText.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.topText)

        self.nameBox = QtWidgets.QWidget()
        self.nameLayout = QtWidgets.QHBoxLayout()
        self.nameBox.setLayout(self.nameLayout)
        self.nameLabel = QtWidgets.QLabel("Name:")
        self.nameLayout.addWidget(self.nameLabel)
        self.nameInput = QtWidgets.QLineEdit(edge.name)
        self.nameInput.textEdited.connect(self.nameChanged)
        self.nameLayout.addWidget(self.nameInput)
        self.layout.addWidget(self.nameBox)


        self.colorBox = QtWidgets.QWidget()
        self.colorLayout = QtWidgets.QHBoxLayout()
        self.colorBox.setLayout(self.colorLayout)
        self.colorLabel = QtWidgets.QLabel("Color:")
        self.colorLayout.addWidget(self.colorLabel)
        self.colorInput = QtWidgets.QPushButton()
        if "color" in edge.data:
            self.colorInput.setStyleSheet("background-color: " + edge.data["color"])
        else:
            self.colorInput.setStyleSheet("background-color: " + "black")
            self.colorInput.setText("None")
        self.colorInput.clicked.connect(self.openColorDialog)
        self.colorLayout.addWidget(self.colorInput)
        self.layout.addWidget(self.colorBox)

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
            if "color" in self.edge.data:
                oldColor = self.edge.data["color"]
            else:
                oldColor = None
                
            if "data" in self.edgeDeltaOld:
                self.edgeDeltaOld["data"]["color"] = oldColor
                self.edgeDeltaNew["data"]["color"] = color.name()
            else:
                self.edgeDeltaOld["data"] = {"color": oldColor}
                self.edgeDeltaNew["data"] = {"color": color.name()}

    def nameChanged(self, event):
        self.edgeDeltaNew["name"] = event
        if "name" not in self.edgeDeltaOld:
            self.edgeDeltaOld["name"] = self.edge.name
    
    def textChanged(self):
        event = str(self.textInput.toPlainText())
        if "data" in self.edgeDeltaNew:
            self.edgeDeltaNew["data"]["text"] = event
            if not "text" in self.edgeDeltaOld:
                if "text" in self.edge.data:
                    self.edgeDeltaOld["data"] = {"text": self.edge.data["text"]}
                else:
                    self.edgeDeltaOld["data"] = {"text": ""}
        else:
            if "text" in self.edge.data:
                self.edgeDeltaOld["data"] = {"text": self.edge.data["text"]}
            else:
                self.edgeDeltaOld["data"] = {"text": ""}
            self.edgeDeltaNew["data"] = {"text": event}

    def closeApply(self):
        self.apply = True
        self.close()