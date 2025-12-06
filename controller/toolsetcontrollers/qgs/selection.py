
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

The Selection class will watch for layer changed signals, and will also watch
for selection changed signals on the active layer using the Layer class.

The selection.changed signal will emit when:
- the layerselection is changed, or
- the featureselection is changed (regardless of visibility).
The layer property may be None.
'''

class Selection(QObject):
    changed = pyqtSignal(object)

    def __init__(self, iface):
        super().__init__()
        self._iface = iface
        self._iface.currentLayerChanged.connect(self.currentLayerChanged)
        self._layer = None

    def __del__(self):
        self._iface.currentLayerChanged.disconnect(self.currentLayerChanged)
        self._iface = None

    def currentLayerChanged(self, layer):
        self._layer = None
        if hasattr(layer, 'selectionChanged'):
            self._layer = Layer(layer)
            self._layer.selectedFeaturesChanged.connect(self.changed)
        self.changed.emit(layer)

################################################################################

class Layer(QObject):
    selectedFeaturesChanged = pyqtSignal(object)

    def __init__(self, layer):
        super().__init__()
        self._layer = layer
        self._layer.selectionChanged.connect(self.selectionChanged)

    def selectionChanged(self, *args):
        self.selectedFeaturesChanged.emit(self._layer)

################################################################################

