from PyQt5 import QtWidgets, QtGui, QtCore
import draggableWidget

class QRegionWidget(draggableWidget.QDragWidget):
    def __init__(self, id: int, name: str, position: list, size: QtCore.QPoint(), color=None, parent=None):
        super().__init__(parent=parent)

        self.parent = parent

        assert(type(id) == int)
        assert(type(name) == str)
        assert(type(position) == list)
        assert(type(size) == QtCore.QPoint)
        self.id = id
        self.name = name
        self.position = position
        self.widgetPosition = position
        self.size = size
        self.color = color
        self.captured = []

        self.moveNode(self.position[0], self.position[1])

        self.resize(0,0)

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

    def calculateCaptured(self):
        self.captured = []
        for node in self.parent.nodes.values():
            # Bounds checking
            # Yes, this is ugly, but who cares
            if self.pos().x() <= node.pos().x() <= self.pos().x() + self.size.x() and self.pos().x() <= node.pos().x() + 100 <= self.pos().x() + self.size.x():
                if self.pos().y() <= node.pos().y() <= self.pos().y() + self.size.y() and self.pos().y() <= node.pos().y() + 100 <= self.pos().y() + self.size.y():
                    self.captured.append(node.id)

    def updateName(self, newName, test=False):
        self.parent.stateMachine.editNode(self.id, {"name": self.name}, {"name": newName}, origin="regionWidget.py:updateName")
        self.name = newName
        self.parent.update()
    
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        self.dragRight = False
        self.dragLeft = False
        self.freeDrag = False
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            self.startPos = event.globalPos()
            self.startMapperPos = self.position
            self.moveOffset = event.globalPos() - self.pos()
            self.parent.updateSelection(self)
        if event.button() == QtCore.Qt.RightButton:
            self.startPos = event.globalPos()
            self.dragRight = True


    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            if (globalPos - self.startPos).manhattanLength() > 30 or self.freeDrag:
                self.dragLeft = True
                self.freeDrag = True
                if self.parent.gridEnabled: # TODO: Fix this to use correct offset
                    pos1 = self.parent.mapFromGlobal(globalPos)
                    localGridSize = self.parent.gridSize * self.parent.zoomLevel
                    diff = globalPos - self.__mouseMovePos
                    #newPos = self.mapFromGlobal(currPos + diff)
                    newPos = pos1 - self.moveOffset
                    originalPos = self.pos()
                    self.moveNode(
                        round(newPos.x() / localGridSize)*localGridSize - (localGridSize - (self.parent.offset.x() % localGridSize)),
                        round(newPos.y() / localGridSize)*localGridSize - (localGridSize - (self.parent.offset.y() % localGridSize))
                    )
                    #self.moveNode(
                    #    round(newPos.x() / localGridSize) * localGridSize - (localGridSize - (self.parent.offset.x() % localGridSize)),
                    #    round(newPos.y() / localGridSize) * localGridSize - (localGridSize - (self.parent.offset.y() % localGridSize))
                    #)
                    #self.moveNode(newPos.x(), newPos.y())
                    for id in self.captured:
                        node = self.parent.nodes[id]
                        node.moveDelta(self.pos().x() - originalPos.x(), self.pos().y() - originalPos.y())
                else:
                    diff = globalPos - self.__mouseMovePos
                    newPos = self.mapFromGlobal(currPos + diff)
                    self.moveNode(newPos.x(), newPos.y())
                    for id in self.captured:
                        node = self.parent.nodes[id]
                        node.moveDelta(diff.x(), diff.y())
                self.parent.update()
                self.__mouseMovePos = globalPos
        elif event.buttons() == QtCore.Qt.RightButton:
            #self.parent.tempLine = 1
            self.parent.tempLine = [self.center, event.windowPos()]
            #self.parent.tempLine.setLine(self.center.x(), self.center.y(), event.windowPos().x(), event.windowPos().y())
            self.parent.update() 

        #super(DragButton, self).mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.parent.tempLine = None
        self.parent.update()
        if self.dragRight:
            self.dragRight = False
            x = event.windowPos().x()
            y = event.windowPos().y()
            found = None
            for node in self.parent.nodes.values():
                if node.widgetPosition[0] < x < node.widgetPosition[0] + node.width():
                    if node.widgetPosition[1] < y < node.widgetPosition[1] + node.height():
                        found = node
            if found is not None:
                self.parent.addConnection(self, found)

        elif self.dragLeft:
            deltaOld = {"position": self.startMapperPos}
            #deltaNew = {"position": self.position}
            x = [
                self.position[0] * self.parent.zoomLevel,
                self.position[1] * self.parent.zoomLevel,
            ]
            deltaNew = {"position": [self.position[0], self.position[1]]}
            self.position = deltaNew["position"]
            print(deltaNew["position"], "     ", self.position)
            self.parent.stateMachine.editNode(self.id, deltaOld, deltaNew, origin="nodeWidget.py:mouseReleaseEvent")

        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

    def customResizeEvent(self, event, sides):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            if (globalPos - self.startPos).manhattanLength() > 30 or self.freeDrag:
                self.dragLeft = True
                self.freeDrag = True
                """if self.parent.gridEnabled:
                    pos1 = self.parent.mapFromGlobal(globalPos)
                    localGridSize = self.parent.gridSize * self.parent.zoomLevel
                    self.moveNode(
                        round(pos1.x() / localGridSize)*localGridSize - (localGridSize - (self.parent.offset.x() % localGridSize)),
                        round(pos1.y() / localGridSize)*localGridSize - (localGridSize - (self.parent.offset.y() % localGridSize))
                    )
                else:
                    diff = globalPos - self.__mouseMovePos
                    newPos = self.mapFromGlobal(currPos + diff)
                    self.moveNode(newPos.x(), newPos.y())"""

                delta = globalPos - self.__mouseMovePos
                diff = delta
                posDiff = QtCore.QPoint(0, 0)
                if not (sides[0] or sides[1]):
                    diff.setX(0)
                if not (sides[2] or sides[3]):
                    diff.setY(0)
                if sides[0]:
                    posDiff.setX(delta.x())
                    diff.setX(-delta.x())
                if sides[2]:
                    posDiff.setY(delta.y())
                    diff.setY(-delta.y())
                newPos = self.mapFromGlobal(currPos + posDiff)
                self.moveNode(newPos.x(), newPos.y())

                newSize = self.size + diff
                self.size = newSize

                self.parent.update()
                self.__mouseMovePos = globalPos
        elif event.buttons() == QtCore.Qt.RightButton:
            #self.parent.tempLine = 1
            self.parent.tempLine = [self.center, event.windowPos()]
            #self.parent.tempLine.setLine(self.center.x(), self.center.y(), event.windowPos().x(), event.windowPos().y())
            self.parent.update()