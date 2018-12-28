import sys, pickle
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from simo_objects import SimoPath, SimoObject
from save_and_load import parseScene

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        # Graphics scene
        self.scene = GraphicsScene()
        self.view = GraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.view.show()

        # Actions
        exitAction = QAction('Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        saveAction = QAction('Save scene', self)
        saveAction.setStatusTip('Save scene')
        saveAction.triggered.connect(self.saveScene)

        loadAction = QAction('Load scene', self)
        loadAction.setStatusTip('Load scene')
        loadAction.triggered.connect(self.loadScene)

        listAction = QAction('List', self)
        listAction.setStatusTip('List items')
        listAction.triggered.connect(self.listItems)

        printSelectedAction = QAction('Selected', self)
        printSelectedAction.setStatusTip('Print Selected items')
        printSelectedAction.triggered.connect(self.printSelected)

        addSObjectAction = QAction('SObject', self)
        addSObjectAction.setStatusTip('Add SObject')
        addSObjectAction.triggered.connect(self.drawSObject)

        addSPathAction = QAction('SPath', self)
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
        rect = QRectF(-100, -100, 50, 50)
        self.scene.addItem(SimoObject(rect, self.scene))

    def drawSPath(self):
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(200, 100)
        self.scene.addItem(SimoPath(path, self.scene))

class GraphicsScene(QGraphicsScene):
    grid = 30

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        #self.setSceneRect(0, 0, 1000, 1000)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, QColor(30, 30, 30))
        left = int(rect.left()) - int((rect.left()) % self.grid)
        top = int(rect.top()) - int((rect.top()) % self.grid)
        right = int(rect.right())
        bottom = int(rect.bottom())
        lines = []
        for x in range(left, right, self.grid):
            lines.append(QLine(x, top, x, bottom))
        for y in range(top, bottom, self.grid):
            lines.append(QLine(left, y, right, y))
        painter.setPen(QPen(QColor(50, 50, 50)))
        painter.drawLines(lines)
    
class GraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(GraphicsView, self).__init__(scene, parent)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)

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
        print(event.key(), event.text())
        if event.modifiers() == Qt.ControlModifier:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        if event.key() == Qt.Key_Delete:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        super(GraphicsView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == 16777249: # ctrl
            self.setDragMode(QGraphicsView.RubberBandDrag)
        super(GraphicsView, self).keyReleaseEvent(event)

    def wheelEvent(self, event):
        modifiers = QGuiApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            self.zoom(event)
        super(GraphicsView, self).wheelEvent(event)

    #def mouseMoveEvent(self, event):

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(600, 600)
    main_window.show()
    sys.exit(app.exec_())