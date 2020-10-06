from PyQt5 import QtWidgets, QtGui, QtCore

import nodeDetailDialog

class QDragWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.parent = parent

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
            self.parent.updateSelection(self)
        if event.button() == QtCore.Qt.RightButton:
            self.startPos = event.globalPos()
            self.dragRight = True

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            if (globalPos - self.startPos).manhattanLength() > 30 or self.freeDrag:
                self.dragLeft = True
                self.freeDrag = True
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                self.moveNode(newPos.x(), newPos.y())
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
                    if node.widgetPosition[1] < y < node.widgetPositionA[1] + node.height():
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

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            dialog = nodeDetailDialog.QNodeDetailDialog(self)
            dialog.exec()
            if dialog.apply:
                self.parent.stateMachine.editNode(self.id, dialog.nodeDeltaOld, dialog.nodeDeltaNew, origin="nodeWidget.py:mouseDoubleClickEvent")
                self.applyChange(dialog.nodeDeltaNew)