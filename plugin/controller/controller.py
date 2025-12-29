

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS()


################################################################################
### Toolbar
################################################################################

class ToolBar:
    _NAME = "Feature Navigation Toolbar"
    _GUID = _IDENTITY.PREFIX+_NAME.replace(" ", "")

    def __new__(cls, iface):
        toolBar = iface.addToolBar(_LABELS(cls._NAME))
        toolBar.setObjectName(cls._GUID)
        return toolBar

################################################################################

import random

from qgis.core import *
from qgis.PyQt.QtCore import *

from .toolsetcontrollers import ResetController
from .toolsetcontrollers import IndexController
from .dialog import ResetDialog

################################################################################
### NavigationController
################################################################################
'''
Controller is the main controller.
It merely manages two subcontrollers that do the actual work.

Controller
    ResetController <-- responsible for reset button
        ResetTools
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

        self._iface = iface
        self._resetController = ResetController(iface, toolBar)
        self._indexController = IndexController(iface, toolBar)

        self._resetController.setDelegate(self)
        self._indexController.didSelectFeature.connect(self.didSelectFeature)

        self._iface.setProperty(self._GUID, self)

    def __del__(self):
        self._iface.setProperty(self._GUID, None)

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
    ### ResetController delegation
    ########################################################################

    def validateReset(self, layer):
        enable = self._indexController.validateLayer(layer)
        self._resetController.setEnabled(enable)

    def resetClicked(self, layer):
        if self._indexController.validateLayer(layer):
            if self.confirmReset(layer):
                self._indexController.setLayer(layer)

    ########################################################################
    '''
    Resetting the current session is potentially prohibitive. The user may have
    had an elaborate selection set for browsing. Recreating the selection may
    be expensive. We therefore want to double check a reset.

    TODO some scenarios might even require a disabled/locked reset button?
    '''
    def confirmReset(self, layer):
        parent = self._iface.mainWindow()
        sample = ResetDialog(parent).confirmReset(layer)
        if sample is not None:
            if 2 <= sample < layer.selectedFeatureCount():
                A = layer.selectedFeatureIds()
                A = random.sample(A, k=sample)
                layer.selectByIds(A)
            return True
        return False
