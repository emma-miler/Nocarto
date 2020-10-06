from PyQt5 import QtWidgets, QtGui, QtCore

import nodeDetailDialog
import draggableWidget


class QAnchorWidget(draggableWidget.QDragWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.parent = parent
        self.position = [0,0]
        self.widgetPosition = self.position

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(QtCore.QMargins(5, 5, 5, 5))
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setLayout(self.layout)
        self.mainWidget.setStyleSheet("background-color: purple")

        self.show()

    # Moves the node to a new location and updates
    def moveNode(self, x, y):
        self.move(x, y)
        self.position = [x - self.parent.offset.x(), y - self.parent.offset.y()]
        self.widgetPosition = [x, y]
        self.center = QtCore.QPointF(self.widgetPosition[0] + self.width() / 2,
                                     self.widgetPosition[1] + self.height() / 2)

        self.update()

    def moveDelta(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)
        self.widgetPosition = [self.pos().x(), self.pos().y()]
        self.center = QtCore.QPoint(self.widgetPosition[0] + self.width() / 2,
                                    self.widgetPosition[1] + self.height() / 2)