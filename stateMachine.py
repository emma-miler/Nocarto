from PyQt5 import QtWidgets, QtGui, QtCore

# TODO: add support for operations involving multiple nodes, e.g: mass delete

# Action types:
# addNode       (node, data)                    new node created
# deleteNode    (data)                          node deleted
# editNode      (node, oldData, newData)        node's data edited
# addEdge       (edge)                          create edge
# editEdge      (edge, oldData, newData)        edge's data edited
# deleteEdge    (edge)                          edge deleted 

class StateMachine():
    def __init__(self, parent=None):
        self.parent = parent

        self.stateList = []
        self.doOffset = 0 # Holds the current index for undo/redo operations

    def addNode(self, node, data, origin=None):
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append({
            "node": node,
            "data": data,
            "type": "addNode",
            "origin": str(origin)
        })
        self.updateList()
    
    def deleteNode(self, data, origin=None):
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append({
            "data": data,
            "type": "deleteNode",
            "origin": str(origin)
        })
        self.updateList()

    def editNode(self, node, deltaOld, deltaNew, origin=None):
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append({
            "node": node, 
            "old": deltaOld,
            "new": deltaNew,
            "type": "editNode",
            "origin": str(origin),
        })
        self.updateList()
    
    def addEdge(self, edge, origin=None):
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append({
            "node": node,
            "type": "addEdge",
            "origin": str(origin)
        })
        self.updateList()

    def deleteEdge(self, edge, origin=None):
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append({
            "node": node,
            "type": "deleteEdge",
            "origin": str(origin)
        })
        self.updateList()

    def editEdge(self, edge, deltaOld, deltaNew, origin=None):
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append({
            "edge": node, 
            "old": deltaOld,
            "new": deltaNew,
            "type": "editEdge",
            "origin": str(origin),
        })
        self.updateList()

    def updateList(self):
        self.doOffset += 1
        #model = self.parent.parent.listView.model()
        #model.removeRows(0, model.rowCount())
        #for state in self.stateList:
        #    item = QtGui.QStandardItem(str(state))
        #    model.appendRow(item)

    def undo(self):
        if self.doOffset > 0:
            self.doOffset -= 1
            atom = self.stateList[self.doOffset]
            return atom
        else:
            return None