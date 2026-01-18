

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS({
    "TOOLBAR_TITLE": "Feature Navigation Toolbar"})


################################################################################
### Toolbar
################################################################################

class ToolBar:
    _NAME = "Feature Navigation Toolbar"
    _GUID = _IDENTITY.PREFIX+_NAME.replace(" ", "")

    def __new__(cls, iface):
        toolBar = iface.addToolBar(_LABELS.TOOLBAR_TITLE)
        toolBar.setObjectName(cls._GUID)
        return toolBar

################################################################################

from qgis.core import *
from qgis.PyQt.QtCore import *

from .toolsetcontrollers import ItemsController
from .toolsetcontrollers import IndexController
from .selection import Selection

################################################################################
### NavigationController
################################################################################
'''
Controller is the main controller.
It merely manages two subcontrollers that do the actual work.

Controller
    ItemsController <-- responsible for items menu
        ItemsMenu
    IndexController <-- responsible for index buttons
        IndexTools

The Controller instance is available to other plugins via:

    navCtl = self._iface.property("32bt.fnt.FeatureNavigationController")

Note that an unknown Python object offered to setProperty is likely stored as
an integer. It is therefore not a true weak reference, but will not increase
the refcount either. That means:
    - it is not a circular reference, so __del__ will eventually be called
    - we do need to clear the stored reference ourselves.
'''

class Controller(QObject):
    _NAME = "Feature Navigation Controller"
    _GUID = _IDENTITY.PREFIX+_NAME.replace(" ", "")

    didSelectFeature = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__()
        self.setObjectName(self._GUID)
        self._itemsController = ItemsController(iface, toolBar)
        self._indexController = IndexController(iface, toolBar)

        # Set IndexController as delegate for ItemsController signals
        self._itemsController.setDelegate(self._indexController)
        self._indexController.didSelectFeature.connect(self.didSelectFeature)

        # React to selection changes and sync state
        self._selection = Selection(iface)
        self._selection.changed.connect(self.selectionChanged)
        self.updateActions()

        # Make controller available to other plugins
        self._iface = iface
        self._iface.setProperty(self._GUID, self)

    def __del__(self):
        self._iface.setProperty(self._GUID, None)

    ########################################################################
    ### Selection response
    ########################################################################

    def selectionChanged(self, layer):
        self._itemsController.selectionChanged(layer)
        self._indexController.selectionChanged(layer)
        self.updateActions()

    def updateActions(self):
        self._itemsController.updateActions()
        self._indexController.updateActions()

    ########################################################################
    ### API
    ########################################################################

    def activeLayer(self):
        return self._indexController.layer()

    def selectNextFeature(self, layer=None):
        if layer and layer.isValid():
            if self._indexController.layer() == layer:
                return self._indexController.selectNextFeature()
            layer.removeSelection()

    ########################################################################

