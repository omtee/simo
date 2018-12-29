import sys
import pyside2 as qt
from simo_objects import SimoPath, SimoObject, ObjectNode
from save_and_load import parseScene

class MainWindow(qt.QMainWindow):
    def __init__(self):
        qt.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        # Graphics scene
        self.scene = GraphicsScene()
        self.view = GraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.view.show()

        # Actions
        exitAction = qt.QAction('Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        saveAction = qt.QAction('Save scene', self)
        saveAction.setStatusTip('Save scene')
        saveAction.triggered.connect(self.saveScene)

        loadAction = qt.QAction('Load scene', self)
        loadAction.setStatusTip('Load scene')
        loadAction.triggered.connect(self.loadScene)

        listAction = qt.QAction('List', self)
        listAction.setStatusTip('List items')
        listAction.triggered.connect(self.listItems)

        printSelectedAction = qt.QAction('Selected', self)
        printSelectedAction.setStatusTip('Print Selected items')
        printSelectedAction.triggered.connect(self.printSelected)

        addSObjectAction = qt.QAction('SObject', self)
        addSObjectAction.setStatusTip('Add SObject')
        addSObjectAction.triggered.connect(self.drawSObject)

        addSPathAction = qt.QAction('SPath', self)
        addSPathAction.setStatusTip('Add SPath')
        addSPathAction.triggered.connect(self.drawSPath)
        
        # Menubar
        '''menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(exitAction)
        '''

        # Toolbar
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(exitAction)
        #self.toolbar.addAction(saveAction)
        #self.toolbar.addAction(loadAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(listAction)
        self.toolbar.addAction(printSelectedAction)
        self.toolbar.addSeparator()
        #self.toolbar.addAction(addRectAction)
        #self.toolbar.addAction(addLineAction)
        self.toolbar.addAction(addSObjectAction)
        self.toolbar.addAction(addSPathAction)

        # Statusbar
        self.statusBar().showMessage('Ready')

        # MainWindow
        self.setWindowTitle('My app')

    def saveScene(self):
        pass
        #parseScene(self.scene)

    def loadScene(self):
        pass

    def listItems(self):
        for item in self.scene.items():
            print(item)

    def printSelected(self):
        for item in self.scene.selectedItems():
            print(item)

    def drawSObject(self):
        rect = qt.QRectF(-100, -100, 50, 50)
        self.scene.addItem(SimoObject(rect, self.scene))

    def drawSPath(self):
        path = qt.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(200, 100)
        self.scene.addItem(SimoPath(path, self.scene))

class GraphicsScene(qt.QGraphicsScene):
    grid = 30

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        #self.setSceneRect(0, 0, 1000, 1000)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, qt.QColor(30, 30, 30))
        left = int(rect.left()) - int((rect.left()) % self.grid)
        top = int(rect.top()) - int((rect.top()) % self.grid)
        right = int(rect.right())
        bottom = int(rect.bottom())
        lines = []
        for x in range(left, right, self.grid):
            lines.append(qt.QLine(x, top, x, bottom))
        for y in range(top, bottom, self.grid):
            lines.append(qt.QLine(left, y, right, y))
        painter.setPen(qt.QPen(qt.QColor(50, 50, 50)))
        painter.drawLines(lines)
    
class GraphicsView(qt.QGraphicsView):
    def __init__(self, scene, parent=None):
        super(GraphicsView, self).__init__(scene, parent)

        self.setDragMode(qt.QGraphicsView.RubberBandDrag)
        self.setRenderHint(qt.QPainter.Antialiasing)

    def zoom(self, event):
        anchor = self.transformationAnchor()
        self.setTransformationAnchor(self.AnchorUnderMouse)

        zoom_F = 1.25
        if event.delta() < 0:
            zoom = 1 / zoom_F
        elif event.delta() > 0:
            zoom = zoom_F
        self.scale(zoom, zoom)

        self.setTransformationAnchor(anchor)

    def keyPressEvent(self, event):
        #print(event.key(), event.text())
        if event.modifiers() == qt.Qt.ControlModifier:
            self.setDragMode(qt.QGraphicsView.ScrollHandDrag)
        if event.key() == qt.Qt.Key_Delete:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        super(GraphicsView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == 16777249: # ctrl
            self.setDragMode(qt.QGraphicsView.RubberBandDrag)
        super(GraphicsView, self).keyReleaseEvent(event)

    def wheelEvent(self, event):
        modifiers = qt.QGuiApplication.keyboardModifiers()
        if modifiers == qt.Qt.ControlModifier:
            self.zoom(event)
        super(GraphicsView, self).wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == qt.Qt.LeftButton:
            item = self.itemAt(event.pos())
            if isinstance(item, ObjectNode):
                if self.drawing_line:
                    self.drawing_line = False
                else:
                    print('node')
                    self.drawing_line = True
                    item.add_connection()
        super(GraphicsView, self).mousePressEvent(event)
                

        '''if self.drawing_line:
                self.drawing_line = False
                self.edge.update_p2(event.pos())

            elif self.edge == None:
                self.edge = Edge(self)
                self.drawing_line = True'''

    #def mouseMoveEvent(self, event):

if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(600, 600)
    main_window.show()
    sys.exit(app.exec_())