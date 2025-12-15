

from qgis.core import *
from qgis.PyQt.QtCore import *

################################################################################
### Setup signals
################################################################################
'''
LayerController is the base controller class for our toolscontrollers.
Tools are generally active on a layer and require iface for dialogs & messages.

Class hierarchy toolsetcontrollers:

                                         ResetController
                                       /
    LayerController -> ToolsController - IndexController
      iface              iface         \
      layer              layer           LabelController
                         tools

'''
class LayerController(QObject):
    def __init__(self, iface):
        super().__init__()
        self._iface = iface
        self._layer = None
        self._connect()

    def __del__(self):
        self._disconnect()
        self._layer = None
        self._iface = None
        if hasattr(super(), '__del__'):
            super().__del__()

    ########################################################################

    def iface(self):
        return self._iface

    def layer(self):
        return self._layer

    ########################################################################
    ### Setup signal
    ########################################################################
    '''
    Layers are wrapperobjects and should not be referenced after removal.
    LayerController holds a layer. A layer is a wrapperobject and therefore
    it is only valid until it is removed. Note that even during the signal
    "willBeDeleted", the pythonobject is already unusable and will raise
    a wrapper exception.
    '''
    def _connect(self):
        project = QgsProject.instance()
        project.layersWillBeRemoved.connect(self.layersWillBeRemoved)

    def _disconnect(self):
        project = QgsProject.instance()
        project.layersWillBeRemoved.disconnect(self.layersWillBeRemoved)

    def layersWillBeRemoved(self, idList):
        layer = self.getLayer()
        if layer and layer.id() in idList:
            self.setLayer(None)

    ########################################################################
    '''
    The logic is:
        1. Check if a layer in its current state is **useable**
        2. Adjust GUI accordingly
        3. Set layer if requested
    '''
    # Determine if layer can be used
    def validateLayer(self, layer):
        return bool(layer) and layer.isValid()

    def setLayer(self, layer):
        if self._layer != layer:
            self._layer = layer
            return True
        return False

    # Redundant for balance
    def getLayer(self):
        return self._layer

################################################################################
