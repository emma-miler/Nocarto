from PyQt5 import QtWidgets, QtGui, QtCore
import draggableWidget

class QRegionWidget(draggableWidget.QDragWidget):
    def __init__(self, id: int, name: str, position: list, size: list, color=None, parent=None):
        super().__init__(parent=parent)

        self.parent = parent

        assert(type(id) == int)
        assert(type(name) == str)
        assert(type(position) == list)
        assert(type(size) == list)
        self.id = id
        self.name = name
        self.position = position
        self.widgetPosition = position
        self.size = size
        self.color = color

        self.moveNode(self.position[0], self.position[1])

        if self.color is None:
            self.color = "gray"

        self.update()

        self.show()

    def applyChange(self, delta):
        if "name" in delta:
            self.name = delta["name"]
        if "position" in delta:
            self.moveNode(
                (delta["position"][0] * self.parent.zoomLevel) + self.parent.offset.x(),
                (delta["position"][1] * self.parent.zoomLevel) + self.parent.offset.y(),
                realPos=[delta["position"][0], delta["position"][1]]
            )
        if "size" in delta:
            self.size = delta["size"] if delta["size"] is not None else [250, 250]
        if "color" in delta:
            self.color = delta["color"] if delta["color"] is not None else "gray"

    def updateName(self, newName, test=False):
        self.parent.stateMachine.editNode(self.id, {"name": self.name}, {"name": newName}, origin="regionWidget.py:updateName")
        self.name = newName
        self.parent.update()