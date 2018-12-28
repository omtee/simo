from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

class PathNode(QGraphicsEllipseItem):
    def __init__(self, path, index):
        rad = 3
        super(PathNode, self).__init__(-rad, -rad, 2*rad, 2*rad)

        self.path = path
        self.index = index

        self.setZValue(1)
        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemSendsGeometryChanges |
                      QGraphicsItem.ItemSendsScenePositionChanges)
        self.setBrush(QBrush(Qt.red))
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            self.path.updateElement(self.index, value)
        if change == QGraphicsItem.ItemPositionChange:
            colliding_items = self.collidingItems()
            for item in colliding_items:
                if isinstance(item, ObjectNode):
                    self.setBrush(QBrush(Qt.green))
                    break
            else:
                self.setBrush(QBrush(Qt.red))
        return QGraphicsEllipseItem.itemChange(self, change, value)

    def mouseReleaseEvent(self, event):
        colliding_items = self.collidingItems()
        for item in colliding_items:
            if isinstance(item, ObjectNode):
                self.setBrush(QBrush(Qt.blue))
                if self.parentItem() != item:
                    self.setParentItem(item)
                break
        else:
            self.setBrush(QBrush(Qt.red))
            if self.parentItem() != self.path:
                self.setParentItem(self.path)
        self.setPos(self.parentItem().mapFromScene(event.scenePos()))
        super(PathNode, self).mouseReleaseEvent(event)

class SimoPath(QGraphicsPathItem):
    def __init__(self, path, scene):
        super(SimoPath, self).__init__(path)
        for i in range(path.elementCount()):
            node = PathNode(self, i)
            node.setPos(QPointF(path.elementAt(i)))
            scene.addItem(node)
        self.setPen(QPen(Qt.red, 1.5))

    def updateElement(self, index, pos):
        path = self.path()
        path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(path)

class ObjectNode(QGraphicsRectItem):
    def __init__(self, rect, obj):
        super(ObjectNode, self).__init__(rect, parent=obj)

        self.edges = []

        self.setZValue(1)
        self.setBrush(QBrush(Qt.red))
        self.setPen(QPen(Qt.black, 0.5))

    def mousePressEvent(self, event):
        if event.button == Qt.LeftButton:
            edge = Edge(self)

class Edge(QGraphicsLineItem):
    def __init__(self, source, dest=None, parent=None):
        super(Edge, self).__init__(self, parent)
        self.source = source
        self.dest = dest



class SimoObject(QGraphicsRectItem):
    def __init__(self, rect, scene):
        super(SimoObject, self).__init__(rect)

        rect = self.rect()
        middle_x = rect.top() + rect.height() / 2
        left = rect.left()
        right = rect.right()

        size = 6
        node_left = QRectF(left, middle_x, size, size)
        node_right = QRectF(right, middle_x, size, size)

        self.nodes = []
        self.nodes.append(ObjectNode(node_left, self))
        self.nodes.append(ObjectNode(node_right, self))

        self.setFlags(QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsSelectable)

    def __getstate__(self):
        return self.rect()