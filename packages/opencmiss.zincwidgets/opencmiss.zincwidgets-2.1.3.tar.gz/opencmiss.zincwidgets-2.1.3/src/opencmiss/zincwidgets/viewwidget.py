
from PySide2 import QtCore, QtWidgets

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget


class ViewWidget(QtWidgets.QWidget):

    graphicsReady = QtCore.Signal()
    currentChanged = QtCore.Signal()

    def __init__(self, scenes, grid_description=None, parent=None):
        super(ViewWidget, self).__init__(parent)
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self._sceneviewers = []
        self._ready_state = []
        self._initial_state = []
        self._active_sceneviewer = None

        for index, scene in enumerate(scenes):
            s = SceneviewerWidget(self)
            s.graphicsInitialized.connect(self._graphics_initialised)
            s.becameActive.connect(self._active_view_changed)
            self._sceneviewers.append(s)
            self._ready_state.append(False)
            s.setFocusPolicy(QtCore.Qt.StrongFocus)
            row = scene.get("Row", 0)
            col = scene.get("Col", 0)
            self._initial_state.append(scene.get("Sceneviewer", {}))
            layout.addWidget(s, row, col)

    def _active_view_changed(self):
        self._active_sceneviewer = self.sender()
        layout = self.layout()
        rows = layout.rowCount()
        columns = layout.columnCount()
        for r in range(rows):
            for c in range(columns):
                sceneviewer_widget = layout.itemAtPosition(r, c).widget()
                sceneviewer_widget.setActiveState(sceneviewer_widget == self.sender())

        self.currentChanged.emit()

    def _graphics_initialised(self):
        index = self._sceneviewers.index(self.sender())
        self._initial_state[index].applyParameters(self.sender().getSceneviewer())
        if self._active_sceneviewer is None:
            self._active_view_changed()
        self._ready_state[index] = True
        if all(self._ready_state):
            self.graphicsReady.emit()

    def getSceneviewer(self, row, col):
        layout = self.layout()
        sceneviewer_widget = layout.itemAtPosition(row, col).widget()
        return sceneviewer_widget.getSceneviewer()

    def getActiveSceneviewer(self):
        if self._active_sceneviewer is not None:
            return self._active_sceneviewer.getSceneviewer()

        return None

    def setContext(self, context):
        for sceneviewer in self._sceneviewers:
            sceneviewer.setContext(context)
