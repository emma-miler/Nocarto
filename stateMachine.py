from PyQt5 import QtWidgets, QtGui, QtCore

# Action types:
# Name          Parameters                      Description
# addNode       (node, data)                    new node created
# deleteNode    (data)                          node deleted
# editNode      (node, oldData, newData)        node's data edited
# addEdge       (edge)                          create edge
# editEdge      (edge, oldData, newData)        edge's data edited
# deleteEdge    (edge)                          edge deleted
# moveRegion    (region, oldPos, newPos, captured)

class StateMachine:
    def __init__(self, parent=None):
        self.parent = parent

        self.undoList = []
        self.redoList = []
        self.doOffset = 0 # Holds the current index for undo/redo operations

    def checkOffset(self):
        if len(self.redoList) > 0:
            self.redoList = []

    def addNode(self, data, origin=None):
        self.checkOffset()
        self.undoList.append({
            "data": data,
            "type": "addNode",
            "origin": str(origin)
        })
        self.updateList()
    
    def deleteNode(self, data, edges=None, origin=None):
        self.checkOffset()
        self.undoList.append({
            "data": data,
            "edges": edges,
            "type": "deleteNode",
            "origin": str(origin)
        })
        self.updateList()

    def editNode(self, id, deltaOld, deltaNew, origin=None):
        self.checkOffset()
        self.undoList.append({
            "id": id,
            "old": deltaOld,
            "new": deltaNew,
            "type": "editNode",
            "origin": str(origin),
        })
        self.updateList()
    
    def addEdge(self, edge, origin=None):
        self.checkOffset()
        self.undoList.append({
            "edge": edge,
            "type": "addEdge",
            "origin": str(origin)
        })
        self.updateList()

    def deleteEdge(self, edge, origin=None):
        self.checkOffset()
        self.undoList.append({
            "edge": edge,
            "type": "deleteEdge",
            "origin": str(origin)
        })
        self.updateList()

    def editEdge(self, edge, deltaOld, deltaNew, origin=None):
        self.checkOffset()
        self.undoList.append({
            "edge": edge, 
            "old": deltaOld,
            "new": deltaNew,
            "type": "editEdge",
            "origin": str(origin),
        })
        self.updateList()

    def moveRegion(self, region, oldPos, newPos, captured, origin=None):
        self.checkOffset()
        self.undoList.append({
            "region": region,
            "old": oldPos,
            "new": newPos,
            "captured": captured,
            "type": "moveRegion",
            "origin": str(origin),
        })
        self.updateList()

    def updateList(self):
        self.doOffset += 1
        #model = self.parent.parent.listView.model()
        #model.removeRows(0, model.rowCount())
        #for state in self.undoList:
        #    item = QtGui.QStandardItem(str(state))
        #    model.appendRow(item)

    def undo(self):
        if len(self.undoList) > 0:
            atom = self.undoList.pop()
            self.redoList.append(atom)
            return atom
        else:
            return None

    def redo(self):
        if len(self.redoList) > 0:
            atom = self.redoList.pop()
            self.undoList.append(atom)
            return atom
        else:
            return None