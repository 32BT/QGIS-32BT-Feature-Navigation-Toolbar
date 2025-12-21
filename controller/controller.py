

from .. import IDENTITY as PLUGIN


################################################################################
### Toolbar
################################################################################

from ..language import _str

class ToolBar:
    _NAME = "Feature Navigation Toolbar"
    _GUID = PLUGIN.PREFIX+_NAME.replace(" ", "")

    def __new__(cls, iface):
        toolBar = iface.addToolBar(_str(cls._NAME))
        toolBar.setObjectName(cls._GUID)
        return toolBar

################################################################################

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
    _GUID = PLUGIN.PREFIX+_NAME.replace(" ", "")

    didSelectFeature = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__()
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
    def confirmReset(self, new_layer):
        old_layer = self._indexController.layer()
        if old_layer is None:
            # Reset from None means there was no active session
            return True
        else:
            # There is an active session, ask confirmation
            parent = self._iface.mainWindow()
            return ResetDialog(parent).confirmReset(old_layer, new_layer)


