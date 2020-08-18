from PyQt5 import QtWidgets, QtGui, QtCore

# TODO: add support for operations involving multiple nodes, e.g: mass delete

# Action types:
# addNode       (node)                          new node created
# deleteNode    (node)                          node deleted
# editNode      (node, oldData, newData)        node's data edited
# addEdge       (edge, node1, node2)            create edge
# editEdge      (edge, oldData, newData)        edge's data edited
# deleteEdge    (edge)                          edge deleted 

class StateMachine():
    def __init__(self, parent=None):
        self.parent = parent

        self.stateList = []
        self.doOffset = 0 # Holds the current index for undo/redo operations

    def pushChange(self, node, deltaOld, deltaNew, actionType, origin=None):
        #if deltaOld == deltaNew:
        #    return
        # TODO: implement overwriting redo when in the past
        if self.doOffset < len(self.stateList):
            self.stateList = self.stateList[:self.doOffset]
        self.stateList.append( {
            "node": node, 
            "old": deltaOld,
            "new": deltaNew,
            "type": actionType,
            "origin": origin,
        })
        self.doOffset += 1
    
    def undo(self):
        if self.doOffset > 0:
            self.doOffset -= 1
            atom = self.stateList[self.doOffset]
            return atom
        else:
            return None