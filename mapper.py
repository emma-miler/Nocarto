import random
from PyQt5 import QtWidgets, QtCore, QtGui

import nodeWidget, edgeWidget
import stateMachine
import fileIO
import edgeDetailDialog
import redirectWidget

class OverlayWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumSize(500, 500)

        self.parent=parent

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        self.circleSize = 20
        self.hcs = int(self.circleSize / 2)

        self.graphicsView = QtWidgets.QGraphicsView(self)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.button = QtWidgets.QPushButton("test123")

        self.w = self.scene.addWidget(self.button)
        self.w.setPos(100, 100)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        #qp.fillRect(0, 0, 1000, 1000, QtGui.QBrush(QtGui.QColor(0, 64, 0)))
        qp.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        qp.drawText(0, 50, f"Edges on screen: {str(len(self.parent.edges))}")
        for nodeId in self.parent.nodes:
            node = self.parent.nodes[nodeId]
            pos = node.position
            qp.drawEllipse(pos[0] - self.hcs,                   pos[1] + node.height()/2 - self.hcs,    self.circleSize,    self.circleSize)
            qp.drawEllipse(pos[0] + node.width() - self.hcs,    pos[1] + node.height()/2 - self.hcs,    self.circleSize, self.circleSize)
            qp.drawEllipse(pos[0] + node.width()/2 - self.hcs,  pos[1]- self.hcs,                       self.circleSize,    self.circleSize)
            qp.drawEllipse(pos[0] + node.width()/2 - self.hcs,  pos[1] + node.height() - self.hcs,      self.circleSize, self.circleSize)
        qp.end()

class FreeFormMap(QtWidgets.QWidget):
    def __init__(self, map=None, mapType=None, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.nodes = {} # List of all nodes, with their id as the key
        self.edges = [] # List of edges currently being drawn
        self.mapNodes = map["nodes"] if map is not None else []
        self.mapEdges = map["edges"] if map is not None else []

        self.enableAA = False
        self.inEditMode = False

        self.selected = None # Holds selected node

        self.root = None # Holds root node in a mindmap

        self.polies = []

        self.offset = QtCore.QPoint()
        self.zoomLevel = 100

        # Set up state machine
        self.stateMachine = stateMachine.StateMachine(parent=self)

        if mapType == "mindmap":
            if map is not None:
                for node in self.mapNodes:
                    # TODO: implement positioning for mindmaps
                    pos = [300, 300]
                    if node["data"]["parent"] is None:
                        pos = [int(self.width()/2), int(self.height()/2)]
                    x = self.addNode(node["name"], pos, node["connections"], data=node["data"], id=node["id"])
                    if node["data"]["parent"] is None:
                        self.root = x
        elif mapType == "freemap":
            if map is not None:
                # Adds all of the nodes in the map to the mapper object
                for node in self.mapNodes:
                    self.addNode(node["name"], node["position"], node["connections"], data=node["data"], id=node["id"], push=False)
                # Loops over all edges in the map and applies their data to the correct edges in the mapper object
                for mapedge in self.mapEdges:
                    for edge in self.edges:
                        if [self.nodes[mapedge["node1"]], self.nodes[mapedge["node2"]]] == edge: # Convert from id to nodeWidget and check equality
                            edge.applyChange({"data": mapedge["data"]})

        if map is None:
            self.root = self.addNode("test", [300, 300], None)
            self.root1 = self.addNode("test2", [300, 400], [self.root.id])

        #self.overlay = OverlayWidget(self)

        self.snapMode = False
        self.tempLine = None
    
    def updateSelection(self, newSelection):
        if self.selected is not None:
            if type(self.selected) == nodeWidget.QNodeWidget or type(self.selected) == redirectWidget.QRedirectWidget:
                self.selected.setSelected(False)
            elif type(self.selected) == edgeWidget.QEdgeWidget:
                pass
        if newSelection is not None:
            newSelection.setSelected(True)
        self.selected = newSelection

    def addNode(self, name, position, connections, data=None, id=None, push=True):
        # Generate a random id
        if id is None:
            newId = random.randint(0, 65535)

            # Check if it is unique, if not, generate a new one and repeat until unique is found
            idIsUnique = True
            for node in self.nodes.values():
                if node.id == newId:
                    idIsUnique = False
            while idIsUnique is False:
                newId = random.randint(0, 65535)
                for node in self.nodes.values():
                    if node.id == newId:
                        idIsUnique = False

        else:
            newId = id

        # Instantiate the node and update possible parents or add to roots list
        connectionList = connections if connections is not None else []
        if data is not None and "isRedirect" in data:
            newNode = redirectWidget.QRedirectWidget(newId, name, position, connectionList, data, parent=self) 
        else:
            newNode = nodeWidget.QNodeWidget(newId, name, position, connectionList, data, parent=self)
        self.nodes[newId] = newNode
        self.buildConnections(newNode)

        if push:
            self.stateMachine.addNode(fileIO.serializeNode(self, newNode), origin="mapper.py:addNode")

        return newNode

    def buildConnections(self, node):
        # Creates connections for existing node
        connections = node.connections
        if connections is not None:
            for connection in connections:
                if connection in self.nodes:
                    self.addConnection(node, self.nodes[connection])

    def addConnection(self, node1, node2):
        for edge in self.edges:
            if edge == (node1, node2):
                return
        node1.connections.append(node2.id)
        node1.connections = list(dict.fromkeys(node1.connections))
        node2.connections.append(node1.id)
        node2.connections = list(dict.fromkeys(node2.connections))
        lineEdit = QtWidgets.QLineEdit(self)
        edge = edgeWidget.QEdgeWidget("", node1, node2, lineEdit, parent=self)
        #self.graphicsScene.addItem(edge)
        #self.graphicsScene.addWidget(widget)
        self.edges.append(edge)
        self.update()
    
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, self.enableAA)
        qp.setPen(QtGui.QPen(QtGui.QColor(128, 255, 128), 10))

        self.polies = []

        if self.tempLine is not None:
            qp.drawLine(self.tempLine[0], self.tempLine[1])

        qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 0), 15))

        for edge in self.edges:
            for poly in edge.generatePolys():
                path = QtGui.QPainterPath()
                color = QtGui.QColor(edge.color) if edge.color is not None else QtGui.QColor(128, 255, 128)
                color = QtGui.QColor(255, 255, 255) if self.selected is edge else color
                qp.setBrush(color)
                path.setFillRule(QtCore.Qt.WindingFill)
                path.addPolygon(poly[0])
                qp.drawPath(path)

        qp.drawText(0,50, f"Edges on screen: {str(len(self.edges))}")

        qp.setPen(QtGui.QPen(QtGui.QColor(255, 128, 128), 10))
        qp.drawEllipse(self.offset, 10, 10)

        qp.end()

    def createNewNode(self):
        connection = [] if self.selected is None else [self.selected.id]
        # noinspection PyUnresolvedReferences
        pos = [300, 300] if self.selected is None else [self.selected.position[0], self.selected.position[1] + 150]
        self.addNode("", pos, connection)

    def setEditNode(self, edit):
        if self.selected is not None:
            if edit is True:
                self.inEditMode = True
                if type(self.selected) == nodeWidget.QNodeWidget:
                    self.selected.label.hide()
                    self.selected.textEdit.show()
                    self.selected.textEdit.setFocus()
            else:
                self.inEditMode = False
                if type(self.selected) == nodeWidget.QNodeWidget:
                    newText = self.selected.textEdit.text()
                    self.selected.text = newText
                    self.selected.label.setText(newText)
                    self.selected.label.show()
                    self.selected.textEdit.hide()
                else:
                    pass
            self.selected.update()
            self.update()

    def setEditEdge(self, edit):
        if self.selected is not None:
            if edit is True:
                self.inEditMode = True
                self.selected.label.hide()
                self.selected.textEdit.show()
                self.selected.textEdit.setFocus()
            else:
                self.inEditMode = False
                newText = self.selected.textEdit.text()
                self.selected.text = newText
                self.selected.label.setText(newText)
                self.selected.label.show()
                self.selected.textEdit.hide()
            self.selected.update()
            self.update()

    def deleteNode(self, node):
        res = list(filter(lambda filterEdge: filterEdge.node1 != node and filterEdge.node2 != node, self.edges))
        other = list(filter(lambda filterEdge: filterEdge.node1 == node or filterEdge.node2 == node, self.edges))
        for edge in other:
            edge.destroy()
            del edge
        self.edges = res
        self.nodes.pop(node.id)
        node.setParent(None)
        node.deleteLater()
        self.updateSelection(None)
        self.update()
    
    def deleteCurrentNode(self):
        if self.selected is not None:
            connections = []
            for node in self.nodes.values():
                if node is not self.selected:
                    if self.selected.id in node.connections:
                        connections.append(node.id)
            self.selected.connections = connections
            # When deleting a node, we save its serialized data to the state machine so we can rebuild it later
            connectedEdges = list(filter(lambda filterEdge: filterEdge.node1 == node or filterEdge.node2 == node, self.edges))
            serialized = []
            for edge in connectedEdges:
                serialized.append(fileIO.serializeEdge(edge))
            self.stateMachine.deleteNode(fileIO.serializeNode(self, self.selected), serialized)
            self.deleteNode(self.selected)

    def rebuildNode(self, data):
        self.addNode(data["name"], data["position"], data["connections"], data=data["data"], id=data["id"], push=False)
        self.update()

    def undo(self):
        atom = self.stateMachine.undo()
        if atom is not None:
            print(atom)
            if atom["type"] == "editNode":
                self.nodes[atom["id"]].applyChange(atom["old"])
            elif atom["type"] == "addNode":
                self.deleteNode(self.nodes[atom["data"]["id"]])
            elif atom["type"] == "deleteNode":
                self.rebuildNode(atom["data"])
            elif atom["type"] == "editEdge":
                atom["edge"].applyChange(atom["old"])
            elif atom["type"] == "addEdge":
                self.deleteEdge(atom["old"])
            elif atom["type"] == "deleteEdge":
                self.rebuildEdge(atom["old"])
            else:
                raise NotImplementedError("Atom type not yet implemented")
            self.update()

    def redo(self):
        atom = self.stateMachine.redo()
        if atom is not None:
            print(atom)
            if atom["type"] == "editNode":
                self.nodes[atom["id"]].applyChange(atom["new"])
            elif atom["type"] == "deleteNode":
                self.deleteNode(self.nodes[atom["data"]["id"]])
            elif atom["type"] == "addNode":
                print(atom["data"])
                self.rebuildNode(atom["data"])
            elif atom["type"] == "editEdge":
                atom["edge"].applyChange(atom["new"])
            elif atom["type"] == "deleteEdge":
                self.deleteEdge(atom["old"])
            elif atom["type"] == "addEdge":
                self.rebuildEdge(atom["old"])
            else:
                raise NotImplementedError("Atom type not yet implemented")
            self.update()

    def mouseDoubleClickEvent(self, event):
        localPos = QtCore.QPoint(event.windowPos().x(), event.windowPos().y() - 15)
        for poly in self.polies:
            if poly[0].containsPoint(localPos, QtCore.Qt.OddEvenFill) or poly[1].containsPoint(localPos, QtCore.Qt.OddEvenFill):
                if event.buttons() == QtCore.Qt.LeftButton:
                    dialog = edgeDetailDialog.QEdgeDetailDialog(poly[2])
                    dialog.exec()
                    if dialog.apply:
                        self.stateMachine.editEdge(poly[2], dialog.edgeDeltaOld, dialog.edgeDeltaNew,
                                                          origin="edgeWidget.py:mouseDoubleClickEvent")
                        poly[2].applyChange(dialog.edgeDeltaNew)
                    self.update()

    def mousePressEvent(self, event):
        localPos = QtCore.QPoint(event.windowPos().x(), event.windowPos().y() - 15)
        self.setFocus()
        self.setEditNode(False)
        self.updateSelection(None)
        for poly in self.polies:
            if poly[0].containsPoint(localPos, QtCore.Qt.OddEvenFill) or poly[1].containsPoint(localPos, QtCore.Qt.OddEvenFill):
                if event.buttons() == QtCore.Qt.LeftButton:
                    self.selected = poly[2]
        self.update()
        if self.selected is None and event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            self.startPos = event.globalPos()
            self.freeDrag = False

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            if (globalPos - self.startPos).manhattanLength() > 5 or self.freeDrag:
                self.freeDrag = True
                diff = globalPos - self.__mouseMovePos
                delta = self.mapFromGlobal(currPos + diff)
                self.offset += diff
                for node in self.nodes.values():
                    node.moveDelta(diff.x(), diff.y())
                self.__mouseMovePos = globalPos
                print(delta)
        self.update()

    def wheelEvent1(self, event):
        # TODO: make zoom speed customizable
        # TODO: fix this garbage
        self.zoomLevel += event.angleDelta().y() / 15
        x = self.zoomLevel
        self.zoomLevel = max(10, min(self.zoomLevel, 500)) # Clamp zoom level
        if self.zoomLevel == x:
            s = (event.angleDelta().y() / 15) / 100
            for node in self.nodes.values():
                node.updateZoomLevel(self.zoomLevel)
                x0 = ((node.position[0] - self.offset.x()) * s) + (self.offset.x() * s)
                y0 = ((node.position[1] - self.offset.y()) * s) + (self.offset.y() * s)
                node.moveDelta(x0, y0)
        self.update()

    def handleAction(self, action, origin=None):
        if not self.inEditMode:
            if action == "createNode":
                self.createNewNode()
            elif action == "editNode":
                self.setEditNode(True)
            elif action == "deleteNode":
                self.deleteCurrentNode()

    def update(self):
        for edge in self.edges:
            edge.updatePositions()
        super().update()