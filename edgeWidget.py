from PyQt5 import QtWidgets, QtGui, QtCore

import edgeDetailDialog

# TODO: add routing points for line, and maybe make it support beziers

class QEdgeWidget(QtWidgets.QGraphicsLineItem):
    def __init__(self, name, node1, node2, lineEdit: QtWidgets.QLineEdit, data=None, parent=None):
        super().__init__(node1.position[0], node1.position[1], node2.position[0], node2.position[1])
        if data is None:
            data = {}
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.lineEdit = lineEdit
        self.data = data
        self.parent = parent

        self.setAcceptHoverEvents(True)

        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 173); color: black; border: none")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        if self.name == "":
            self.lineEdit.hide()
        self.lineEdit.textEdited.connect(self.updateName)
        self.fm = QtGui.QFontMetrics(self.lineEdit.font())

        self.color = None
        if "color" in self.data:
            self.color = self.data["color"]

        if "name" in self.data:
            self.name = self.data["name"]
            self.lineEdit.setText(self.name)

        self.lineEdit.resize(self.fm.horizontalAdvance(self.lineEdit.text()) + 10, self.fm.height() * 2)

        self.setPen(QtGui.QPen(QtGui.QColor(128, 255, 128), 10))

        self.updatePositions()

        #self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.IBeamCursor)
        #self.lineEdit.resize(self.fm.horizontalAdvance(self.lineEdit.text()) + 0, self.fm.height() * 2)

    def getRepr(self):
        return [self.node1, self.node2]

    def __eq__(self, otherObj):
        on1 = otherObj[0]
        on2 = otherObj[1]
        return (on1 == self.node1 and on2 == self.node2) or (on2 == self.node1 and on1 == self.node2)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            pass

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            dialog = edgeDetailDialog.QEdgeDetailDialog(self)
            dialog.exec()
            if dialog.apply:
                self.parent.stateMachine.editEdge(self, dialog.edgeDeltaOld, dialog.edgeDeltaNew, origin="edgeWidget.py:mouseDoubleClickEvent")
                self.applyChange(dialog.edgeDeltaNew)

    def applyChange(self, delta):
        if "data" in delta:
            newData = delta["data"]
            for item in newData.keys():
                self.data[item] = newData[item]
                if item == "color":
                    print("test")
                    print(newData[item])
                    self.color = newData["color"] if newData["color"] is not None else "gray"
                    self.setPen(QtGui.QPen(QtGui.QColor(self.color), 10))
                if item == "name":
                    self.name = newData[item]
                    self.lineEdit.setText(self.name)
                    self.data["name"] = self.name
                    self.lineEdit.resize(self.fm.horizontalAdvance(self.lineEdit.text()) + 10, self.fm.height() * 2)
                    self.updatePositions()
                    if self.name != "":
                        self.lineEdit.show()

    def updateName(self):
        event = self.lineEdit.text()
        self.parent.stateMachine.editEdge(self, {"name": self.name}, {"name": event}, origin="nodeWidget.py:updateName")
        self.name = event
        self.data["name"] = self.name
        self.lineEdit.resize(self.fm.horizontalAdvance(self.lineEdit.text()) + 10, self.fm.height() * 2)
        self.updatePositions()

    def updatePositions(self):
        n1 = self.node1
        n2 = self.node2
        e1 = n1.position
        e2 = n2.position

        horPos = 0.5
        vertPos = 0.5

        x1 = e1[0] + n1.width() * horPos
        y1 = e1[1] + n1.height() * vertPos
        x2 = e2[0] + n2.width() * (1-horPos)
        y2 = e2[1] + n2.height() * (1-vertPos)
        
        self.setLine(x1, y1, x2, y2)

        self.lineEdit.move(int((x1 + x2) / 2) - int(self.lineEdit.width() / 2), int((y1 + y2) / 2) - int(self.lineEdit.height() / 2))

    def destroy(self):
        self.lineEdit.setParent(None)