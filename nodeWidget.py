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
        self.layout.setContentsMargins(QtCore.QMargins(5, 5, 5, 5))

        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setLayout(self.layout)

        self.mainWidget.resize(100, 100)

        self.center = QtCore.QPoint(0,0)

        self.moveNode(self.position[0], self.position[1])

        self.styleSelected = """
            background-color: white;
            border-radius: 10%;
        """

        self.styleUnselected = """
            background-color: transparent;
            border-radius: 10%;
        """

        self.mainWidget.setStyleSheet(self.styleUnselected)

        self.isSelected = False

        self.color = "gray"
        if "color" in self.data:
            self.color = self.data["color"]
        
        self.label = QtWidgets.QLabel()
        self.label.setText(self.name)
        self.label.setStyleSheet(f"background-color: {self.color}; color: black")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.lFont = self.label.font()

        self.textEdit = QtWidgets.QLineEdit(self.name)
        self.textEdit.setStyleSheet(f"background-color: {self.color}; color: black")
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit.editingFinished.connect(self.updateName)
        self.layout.addWidget(self.textEdit)
        self.textEdit.hide()

        self.update()

        self.show()

    # Make this node the selected node
    # VISUAL CHANGE ONLY!
    def setSelected(self, isSelected):
        self.isSelected = isSelected
        if isSelected:
            self.mainWidget.setStyleSheet(self.styleSelected)
        else:
            self.mainWidget.setStyleSheet(self.styleUnselected)
        self.update()


    # Adds a connection to another node
    def addConnection(self, other):
        self.connections.append(other.id)
        return self

    def applyChange(self, delta):
        if "name" in delta:
            self.name = delta["name"]
            self.label.setText(self.name)
            self.textEdit.setText(self.name)
        if "position" in delta:
            self.moveNode(delta["position"][0], delta["position"][1])
        if "data" in delta:
            newData = delta["data"]
            for item in newData.keys():
                self.data[item] = newData[item]
                if item == "color":
                    print("test")
                    print(newData[item])
                    self.color = newData["color"] if newData["color"] is not None else "gray"
                    self.label.setStyleSheet(f"background-color: {self.color}; color: black")
                    self.textEdit.setStyleSheet(f"background-color: {self.color}; color: black")

    def updateName(self):
        event = self.textEdit.text()
        self.parent.stateMachine.editNode(self.id, {"name": self.name}, {"name": event}, origin="nodeWidget.py:updateName")
        self.name = event
        self.label.setText(event)

    # Moves the node to a new location and updates
    def moveNode(self, x, y):
        self.move(x, y)
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