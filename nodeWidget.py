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
        if data is None:
            self.data = {}

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(QtCore.QMargins(3,3,3,3))

        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setLayout(self.layout)

        self.mainWidget.setMinimumSize(100, 50)

        self.center = QtCore.QPoint(0,0)

        self.moveNode(self.position[0], self.position[1])

        self.styleSelected = """
            background-color: white;
            border-radius: 20px
        """

        self.styleUnselected = """
            background-color: gray;
            border-radius: 20px
        """

        self.mainWidget.setStyleSheet(self.styleUnselected)

        self.isSelected = False
        
        self.label = QtWidgets.QLabel(self.text)
        self.label.setStyleSheet("background-color: gray; color: black")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.textEdit = QtWidgets.QLineEdit(self.text)
        self.textEdit.setStyleSheet("background-color: gray; color: black")
        self.textEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.textEdit)
        self.textEdit.hide()

        self.show()
        self.parent.update()

    # Make this node the selected node
    # VISUAL CHANGE ONLY!
    def setSelected(self, isSelected):
        self.isSelected = isSelected
        if isSelected:
            self.mainWidget.setStyleSheet(self.styleSelected)
        else:
            self.mainWidget.setStyleSheet(self.styleUnselected)


    # Adds a connection to another node
    def addConnection(self, other):
        self.connections.append(other.id)
        return self

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        self.dragRight = False
        self.freeDrag = False
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            self.startPos = event.globalPos()
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
                self.freeDrag = True
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                self.moveNode(newPos.x(), newPos.y())
                self.parent.update()

                self.__mouseMovePos = globalPos
        elif event.buttons() == QtCore.Qt.RightButton:
            #self.parent.tempLine = 1
            self.parent.tempLine = [self.center, event.windowPos()]
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
                if node.position[0] < x < node.position[0] + node.width():
                    if node.position[1] < y < node.position[1] + node.height():
                        found = node
            if found is not None:
                self.parent.addConnection(self, found)

        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        #super(DragButton, self).mouseReleaseEvent(event)

    # Moves the node to a new location and updates
    def moveNode(self, x, y):
        self.move(x, y)
        self.position = [x,y]
        self.center = QtCore.QPoint(self.position[0] + self.width()/2, self.position[1] + self.height()/2)
        self.update()

    # Currently unused draw function
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        #qp.fillRect(0, 0, 100, 100, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        qp.end()
        self.update()