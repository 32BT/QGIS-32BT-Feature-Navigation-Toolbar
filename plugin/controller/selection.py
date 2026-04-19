

from qgis.PyQt.QtCore import *

################################################################################
### Selection
################################################################################
'''
For updating the resetbutton, we need to know if the currently active layer has
a selection. Unfortunately, mapcanvas selectionChanged only emits a signal if
the layer is currently visible, and subsequently changing the visibility does
not emit any signal.

So, we need to implement an alternative...

The Selection class will watch for active layer changes, and will also watch
for selection changes on the active layer, regardless of visibility.

The selection.changed signal will emit when:
- the active layer is switched, or
- the featureselection changes, or
- the active layer changes editing state.

The layer property may be None.
'''

class Selection(QObject):
    changed = pyqtSignal(object)

    def __init__(self, iface):
        super().__init__()
        self._iface = iface
        self._iface.currentLayerChanged.connect(self.setLayer)
        self.setLayer(iface.activeLayer())

    def __del__(self):
        self._iface.currentLayerChanged.disconnect(self.setLayer)
        self._iface = None

    def setLayer(self, layer):
        self._layer = None
        if hasattr(layer, 'selectionChanged'):
            self._layer = Layer(layer)
            self._layer.stateChanged.connect(self.changed)
        self.changed.emit(layer)

################################################################################
'''
'''

class Layer(QObject):
    stateChanged = pyqtSignal(object)

    def __init__(self, layer):
        super().__init__()
        self._layer = layer
        self._layer.selectionChanged.connect(self._stateChanged)
        self._layer.editingStarted.connect(self._stateChanged)
        self._layer.editingStopped.connect(self._stateChanged)

    def _stateChanged(self, *args):
        self.stateChanged.emit(self._layer)

################################################################################
