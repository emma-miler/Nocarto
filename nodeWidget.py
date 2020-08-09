from PyQt5 import QtWidgets, QtGui, QtCore

class QNodeWidget(QtWidgets.QWidget):
    def __init__(self, id: int, text: str, position: tuple or list, connections=None, data=None, parent=None):
        super().__init__(parent=parent)

        #self.setMinimumSize(100,100)

        self.parent = parent

        assert(type(id) == int)
        assert(type(text) == str)
        assert(type(position) == tuple or list)
        assert(type(connections) == list or tuple or connections is None)
        self.id = id
        self.text = text
        self.position = position
        self.connections = connections
        self.data = data

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(QtCore.QMargins(5,5,5,5))

        self.move(self.position[0], self.position[1])

        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setLayout(self.layout)

        self.mainWidget.setMinimumSize(100, 50)

        self.mainWidget.setStyleSheet("""
            background-color: green;
            border-radius: 20px
        """)
        
        self.label = QtWidgets.QLabel(self.text)
        #self.label.setStyleSheet("background-color: red")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.label)

        #self.show()

    def addConnection(self, other):
        self.connections.append(other.id)
        return self

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.startPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        #super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            if (globalPos - self.startPos).manhattanLength() > 30:
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                self.moveNode(newPos.x(), newPos.y())
                self.parent.update()

                self.__mouseMovePos = globalPos
                

        #super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

    def moveNode(self, x, y):
        self.move(x, y)
        self.position = [x,y]
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.fillRect(0, 0, 100, 100, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        qp.end()
        self.update()