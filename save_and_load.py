from PySide2 import QtGui, QtWidgets

def parseScene(scene):
    for item in scene.items():
        print(item.__getstate__)