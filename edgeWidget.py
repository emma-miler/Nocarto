from PyQt5 import QtWidgets, QtGui, QtCore

import edgeDetailDialog

# TODO: add routing points for line, and maybe make it support beziers

class QEdgeWidget():
    def __init__(self, name, node1, node2, lineEdit: QtWidgets.QLineEdit, data=None, parent=None):
        super().__init__()
        if data is None:
            data = {}
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.lineEdit = lineEdit
        self.data = data
        self.parent = parent

        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 173); color: black; border: none")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        if self.name == "":
            self.lineEdit.hide()
        self.lineEdit.textEdited.connect(self.updateName)
        self.lineEdit.focusInEvent = self.lineFocusIn
        self.lineEdit.focusOutEvent = self.lineFocusOut
        self.fm = QtGui.QFontMetrics(self.lineEdit.font())

        self.color = None
        if "color" in self.data:
            self.color = self.data["color"]

        if "name" in self.data:
            self.name = self.data["name"]
            self.lineEdit.setText(self.name)

        self.lineEdit.resize(self.fm.horizontalAdvance(self.lineEdit.text()) + 10, self.fm.height() * 2)

        self.updatePositions()

    def lineFocusIn(self, a0):
        self.lineEdit.selectAll()
        self.lineEdit.update()
        self.parent.selected = self
        self.parent.inEditMode = True

    def lineFocusOut(self, a0):
        self.lineEdit.deselect()
        self.lineEdit.repaint()
        self.parent.selected = None
        self.parent.inEditMode = False

    def getRepr(self):
        return [self.node1, self.node2]

    def __eq__(self, otherObj):
        try:
            on1 = otherObj[0]
            on2 = otherObj[1]
        except TypeError:
            return None
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


        self.lineEdit.move(int((x1 + x2) / 2) - int(self.lineEdit.width() / 2), int((y1 + y2) / 2) - int(self.lineEdit.height() / 2))

    def destroy(self):
        self.lineEdit.setParent(None)

    def generatePolys(self):
        lines = []
        polys = []
        connectionPoints = [self.node1]
        if "redirects" in self.data:
            for redirect in self.data["redirects"]:
                connectionPoints.append(self.parent.nodes[redirect])
            connectionPoints.append(self.node2)
            lines = [[connectionPoints[i], connectionPoints[i+1]] for i in range(len(connectionPoints)-1)]
        else:
            lines = [[self.node1, self.node2]]

        for line in lines:
            n1 = line[0]
            m1 = line[1]
            e1 = n1.position
            e2 = m1.position

            horPos = 0.5
            vertPos = 0.5

            x1 = e1[0] + n1.width() * horPos
            y1 = e1[1] + n1.height() * vertPos
            x2 = e2[0] + m1.width() * (1 - horPos)
            y2 = e2[1] + m1.height() * (1 - vertPos)

            #qp.drawLime(x1, y1, x2, y2)
            poly = QtGui.QPolygonF([
                QtCore.QPointF(x1 - 5, y1),
                QtCore.QPointF(x1 + 5, y1),
                QtCore.QPointF(x2 + 5, y2),
                QtCore.QPointF(x2 - 5, y2),
            ])
            poly1 = QtGui.QPolygonF([
                QtCore.QPointF(x1, y1 - 5),
                QtCore.QPointF(x1, y1 + 5),
                QtCore.QPointF(x2, y2 + 5),
                QtCore.QPointF(x2, y2 - 5),
            ])

            test = poly.united(poly1)
            polys.append([test, self])
        return polys

    def update(self):
        pass