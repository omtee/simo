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
    def __init__(self, rect, obj=None):
        super(ObjectNode, self).__init__(rect, parent=obj)

        self.edge = None
        self.free = True
        self.index = None

        self.setZValue(1)
        self.setFlags(qt.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setBrush(qt.QBrush(qt.Qt.red))
        self.setPen(qt.QPen(qt.Qt.black, 0.5))

    def connect_node(self, node):
        print('connection')
        self.free = False
        self.edge = node.childItems()[0]
        self.index = 2
        self.edge.connect_end(node)
        self.setBrush(qt.QBrush(qt.Qt.green))

    def add_connection(self):
        self.edge = SEdge(self)
        self.parentItem().scene.addItem(self.edge)
        print(self.edge)
        self.index = 1
        self.free = False

    def itemChange(self, change, value):
        if change == qt.QGraphicsItem.ItemScenePositionHasChanged:
            if self.edge:
                self.edge.updateElement(self.index, value)
        return qt.QGraphicsRectItem.itemChange(self, change, value)

class EdgeNode(qt.QGraphicsEllipseItem):
    def __init__(self, edge):
        rad = 3
        super(EdgeNode, self).__init__(-rad, -rad, 2*rad, 2*rad)
        self.setBrush(qt.QBrush(qt.Qt.red))

class SEdge(qt.QGraphicsPathItem):
    def __init__(self, source, dest=None, parent=None):
        self.source = source
        startPoint = self.source.rect().center()
        path = qt.QPainterPath(startPoint)
        #path.lineTo(100, 0)
        super(SEdge, self).__init__(path, parent)

        self.setZValue(1)
        self.setPen(qt.QPen(qt.Qt.white, 0.5))

    def updateElement(self, index, pos):
        pos = self.mapFromScene(pos)
        path = self.path()
        if path.isEmpty():
            path.lineTo(pos)
        path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(path)

    #def updatePath(self, )
    
    def connect_end(self, item):
        self.dest = item

class Edge(qt.QGraphicsLineItem):
    def __init__(self, source, dest=None, parent=None):
        pos_source = source.rect()
        p1 = p2 = pos_source.center()
        line = qt.QLineF(p1, p2)
        super(Edge, self).__init__(line, parent=source)

        self.source = source
        self.dest = dest
        self.setPen(qt.QPen(qt.Qt.gray, 0.5))
    
    def update(self, pos):
        pos = self.parentItem().mapFromScene(pos)
        line = self.line()
        line.setP2(pos)
        self.setLine(line)

    def connect_dest(self, item):
        self.dest = item

class SimoObject(qt.QGraphicsRectItem):
    def __init__(self, rect, scene):
        super(SimoObject, self).__init__(rect)

        self.scene = scene

        rect = self.rect()
        middle_x = rect.top() + rect.height() / 2
        left = rect.left()
        right = rect.right()

        size = 6
        node_left = qt.QRectF(left - size / 2, middle_x - size / 2, size, size)
        node_right = qt.QRectF(right - size / 2, middle_x - size / 2, size, size)

        self.nodes = []
        self.nodes.append(ObjectNode(node_left, self))
        self.nodes.append(ObjectNode(node_right, self))

        self.setFlags(qt.QGraphicsItem.ItemIsMovable |
                      qt.QGraphicsItem.ItemIsSelectable)