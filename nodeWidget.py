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

        self.layout = QtWidgets.QVBoxLayout()
        #self.layout.setContentsMargins(QtCore.QMargins(5, 5, 5, 5))

        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setLayout(self.layout)
        self.mainWidget.setStyleSheet(f"background-color: transparent; color: black")

        #self.mainWidget.resize(100, 100)

        self.center = QtCore.QPoint(0,0)

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
        print("test", test)
        self.parent.stateMachine.editNode(self.id, {"name": self.name}, {"name": newName}, origin="nodeWidget.py:updateName")
        self.name = newName
        self.parent.update()

    # Moves the node to a new location and updates
    def moveNode(self, x, y, realPos=None):
        self.move(x, y)
        if realPos is not None:
            self.position = realPos
        else:
            self.position = [
                (self.widgetPosition[0] - self.parent.offset.x()) / self.parent.zoomLevel,
                (self.widgetPosition[1] - self.parent.offset.y()) / self.parent.zoomLevel,
            ]
        self.widgetPosition = [x,y]
        self.center = QtCore.QPointF(self.widgetPosition[0] + self.width()/2, self.widgetPosition[1] + self.height()/2)

        self.update()

    def moveDelta(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)
        self.widgetPosition = [self.pos().x(), self.pos().y()]
        self.center = QtCore.QPoint(self.widgetPosition[0] + self.width() / 2, self.widgetPosition[1] + self.height() / 2)

    def update(self):
        super().update()
        scale = 100 * self.parent.zoomLevel
        self.mainWidget.resize(scale, scale)
        try:
            pass
            #self.label.setText(str(self.position) + "\n" + str(self.widgetPosition))
        except AttributeError:
            pass
        self.center = QtCore.QPoint(self.widgetPosition[0] + scale / 2, self.widgetPosition[1] + scale / 2)