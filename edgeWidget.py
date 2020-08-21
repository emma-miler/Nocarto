from PyQt5 import QtWidgets, QtGui, QtCore

class QEdgeWidget(QtWidgets.QWidget):
    def __init__(self, name, node1, node2, data=None, parent=None):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.data = data

        self.dead = False

        self.parent = parent

        print(self)

    def getRepr(self):
        return [self.node1, self.node2]
    
    def markDead(self):
        self.dead = True

    def __eq__(self, otherObj):
        on1 = otherObj[0]
        on2 = otherObj[1]
        return (on1 == self.node1 and on2 == self.node2) or (on2 == self.node1 and on1 == self.node2)