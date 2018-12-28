import pyside2 as qt

class PathNode(qt.QGraphicsEllipseItem):
    def __init__(self, path, index):
        rad = 3
        super(PathNode, self).__init__(-rad, -rad, 2*rad, 2*rad)

        self.path = path
        self.index = index

        self.setZValue(1)
        self.setFlags(qt.QGraphicsItem.ItemIsMovable |
                      qt.QGraphicsItem.ItemIsSelectable |
                      qt.QGraphicsItem.ItemSendsGeometryChanges |
                      qt.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setBrush(qt.QBrush(qt.Qt.red))
    
    def itemChange(self, change, value):
        if change == qt.QGraphicsItem.ItemScenePositionHasChanged:
            self.path.updateElement(self.index, value)
        if change == qt.QGraphicsItem.ItemPositionChange:
            colliding_items = self.collidingItems()
            for item in colliding_items:
                if isinstance(item, ObjectNode):
                    self.setBrush(qt.QBrush(qt.Qt.green))
                    break
            else:
                self.setBrush(qt.QBrush(qt.Qt.red))
        return qt.QGraphicsEllipseItem.itemChange(self, change, value)

    def mouseReleaseEvent(self, event):
        colliding_items = self.collidingItems()
        for item in colliding_items:
            if isinstance(item, ObjectNode):
                self.setBrush(qt.QBrush(qt.Qt.blue))
                if self.parentItem() != item:
                    self.setParentItem(item)
                break
        else:
            self.setBrush(qt.QBrush(qt.Qt.red))
            if self.parentItem() != self.path:
                self.setParentItem(self.path)
        self.setPos(self.parentItem().mapFromScene(event.scenePos()))
        super(PathNode, self).mouseReleaseEvent(event)

class SimoPath(qt.QGraphicsPathItem):
    def __init__(self, path, scene):
        super(SimoPath, self).__init__(path)
        for i in range(path.elementCount()):
            node = PathNode(self, i)
            node.setPos(qt.QPointF(path.elementAt(i)))
            scene.addItem(node)
        self.setPen(qt.QPen(qt.Qt.red, 1.5))

    def updateElement(self, index, pos):
        path = self.path()
        path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(path)

class ObjectNode(qt.QGraphicsRectItem):
    def __init__(self, rect, obj):
        super(ObjectNode, self).__init__(rect, parent=obj)

        self.edges = []

        self.setZValue(1)
        self.setBrush(qt.QBrush(qt.Qt.red))
        self.setPen(qt.QPen(qt.Qt.black, 0.5))

    #def mousePressEvent(self, event):
    #    if event.button == qt.Qt.LeftButton:
    #        edge = Edge(self)

class Edge(qt.QGraphicsLineItem):
    def __init__(self, source, dest=None, parent=None):
        super(Edge, self).__init__(self, parent)
        self.source = source
        self.dest = dest



class SimoObject(qt.QGraphicsRectItem):
    def __init__(self, rect, scene):
        super(SimoObject, self).__init__(rect)

        rect = self.rect()
        middle_x = rect.top() + rect.height() / 2
        left = rect.left()
        right = rect.right()

        size = 6
        node_left = qt.QRectF(left, middle_x, size, size)
        node_right = qt.QRectF(right, middle_x, size, size)

        self.nodes = []
        self.nodes.append(ObjectNode(node_left, self))
        self.nodes.append(ObjectNode(node_right, self))

        self.setFlags(qt.QGraphicsItem.ItemIsMovable |
                      qt.QGraphicsItem.ItemIsSelectable)

    def __getstate__(self):
        return self.rect()