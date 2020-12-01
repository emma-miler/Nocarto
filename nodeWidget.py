from PyQt5 import QtWidgets, QtGui, QtCore

import nodeDetailDialog
import draggableWidget

class QNodeWidget(draggableWidget.QDragWidget):
    def __init__(self, id: int, name: str, position: tuple or list, connections=None, data=None, parent=None):
        super().__init__(parent=parent)

        self.parent = parent

        assert(type(id) == int)
        assert(type(name) == str)
        assert(type(position) == tuple or list)
        assert(type(connections) == list or tuple or connections is None)
        self.id = id
        self.name = name
        self.position = position
        self.widgetPosition = position
        self.connections = connections
        self.data = data
        if data is None:
            self.data = {}

        self.center = QtCore.QPoint(0,0)

        self.resize(0, 0)

        self.moveNode(self.position[0], self.position[1])

        self.color = "gray"
        if "color" in self.data:
            self.color = self.data["color"]

        self.update()

        self.show()

    # Adds a connection to another node
    def addConnection(self, other):
        self.connections.append(other.id)
        return self

    def applyChange(self, delta):
        if "name" in delta:
            self.name = delta["name"]
        if "position" in delta:
            self.moveNode(
                (delta["position"][0] * self.parent.zoomLevel) + self.parent.offset.x(),
                (delta["position"][1] * self.parent.zoomLevel) + self.parent.offset.y(),
                realPos=[delta["position"][0], delta["position"][1]]
            )
        if "data" in delta:
            newData = delta["data"]
            for item in newData.keys():
                self.data[item] = newData[item]
                if item == "color":
                    print("test")
                    print(newData[item])
                    self.color = newData["color"] if newData["color"] is not None else "gray"

    def updateName(self, newName, test=False):
        self.parent.stateMachine.editNode(self.id, {"name": self.name}, {"name": newName}, origin="nodeWidget.py:updateName")
        self.name = newName
        self.parent.update()

    def update(self):
        super().update()
        scale = 100 * self.parent.zoomLevel
        try:
            pass
            #self.label.setText(str(self.position) + "\n" + str(self.widgetPosition))
        except AttributeError:
            pass
        self.center = QtCore.QPoint(self.widgetPosition[0] + scale / 2, self.widgetPosition[1] + scale / 2)