
################################################################################
### Toolbar Name
################################################################################

from .language import _str
class TOOLBAR:
    NAME = _str("Feature Navigation Toolbar")

################################################################################

from qgis.PyQt.QtCore import *

from .toolsetcontrollers import ResetController
from .toolsetcontrollers import IndexController
from .dialog import ResetDialog

################################################################################
### NavigationController
################################################################################
'''
NavigationController is the main controller.
It merely manages two subcontrollers that do the actual work.

NavigationController
    ResetController <-- responsible for reset button
        ResetTools
    IndexController <-- responsible for index buttons
        IndexTools

NavigationController is available to other plugins via:

    navCtl = self._iface.property("32bt.fnt.NavigationController")

Note that an unknown Python object offered to setProperty is likely stored as
an integer. It is therefore not a true weak reference, but will not increase
the refcount either. That means:
    - it is not a circular reference, so __del__ will eventually be called
    - we do need to clear the stored reference ourselves.
'''
class NavigationController(QObject):
    didSelectFeature = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__()
        self._iface = iface
        self._resetController = ResetController(iface, toolBar)
        self._indexController = IndexController(iface, toolBar)

        self._resetController.setDelegate(self)
        self._indexController.didSelectFeature.connect(self.didSelectFeature)

        self._iface.setProperty(self.KEY, self)

    def __del__(self):
        self._iface.setProperty(self.KEY, None)

    ########################################################################
    ### API
    ########################################################################

    @property
    def KEY(self):
        return "32bt.fnt."+self.__class__.__name__

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


