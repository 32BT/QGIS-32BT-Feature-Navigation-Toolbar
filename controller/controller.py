
from qgis.PyQt.QtCore import *

from .toolsetcontrollers import ResetController
from .toolsetcontrollers import IndexController
from .dialog import ResetDialog

'''
NavigationController is the main controller.
It merely manages two subcontrollers that do the actual work.

NavigationController
    ResetController <-- responsible for reset button
        ResetTools
    IndexController <-- responsible for index buttons
        IndexTools

NavigationController is derived from KeyController which makes the controller
available to other plugins.
'''

################################################################################
### KeyController
################################################################################
'''
A KeyController is a controller that is publicly reachable from the dynamic
properties of iface using a key. By default, there can be only one instance
of any subclass of KeyController. The construct is meant to be used for
*key* controllers, hence the name. (If more than one instance is ever desired,
then a custom key can be provided.)

Note that an unknown Python object offered to setProperty is likely stored as
an integer. It is therefore not a true weak reference, but will not increase
the refcount either. That means:
    - it is not a circular reference, so __del__ will eventually be called
    - we do need to clear the stored reference ourselves.
'''
class KeyController(QObject):
    @classmethod
    def _get_key(cls, name=None):
        return '.'.join(('32bt','fnt',name or cls.__name__))

    def __init__(self, iface, name=None):
        super().__init__()
        self._KEY = self._get_key(name)
        self._iface = iface
        self._iface.setProperty(self._KEY, self)

    def __del__(self):
        self._iface.setProperty(self._KEY, None)
        if hasattr(super(), '__del__'): super().__del__()

    def find(self, class_name, alt=None):
        return self._iface.property(self._get_key(class_name)) or alt

################################################################################
### NavigationController
################################################################################
'''
The main controller manages the relation between a ResetController and an
IndexController. It is also a KeyController and therefore reachable via a key:

    navCtl = self._iface.property("32bt.fnt.NavigationController")
'''
class NavigationController(KeyController):
    didSelectFeature = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__(iface)
        self._resetController = ResetController(iface, toolBar)
        self._indexController = IndexController(iface, toolBar)

        self._resetController.setDelegate(self)
        self._indexController.didSelectFeature.connect(self.didSelectFeature)

    ########################################################################
    ### API
    ########################################################################
    '''
    This will be called from outside the plugin context. This will:
        - check if incoming layer corresponds to our current layer
        - if so, update selection
        - otherwise remove selection (caller responsibility?)
    '''
    def activeLayer(self):
        return self._indexController.layer()

    def selectNextFeature(self, layer):
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


