

################################################################################
### Plugin Main
################################################################################
'''
Note: unload may be called from a secundary loop like the plugin dialog.
Deleting a toolbar in a secundary loop will not properly remove it from
all UI references, specifically view->toolbars, hence: deleteLater()
'''

from .controller import TOOLBAR_NAME
from .controller import NavigationController

class Plugin:
    def __init__(self, iface):
        self._iface = iface

    def initGui(self):
        self._toolBar = self._iface.addToolBar(TOOLBAR_NAME)
        self._controller = NavigationController(self._iface, self._toolBar)

    def unload(self):
        self._controller = None
        self._toolBar.deleteLater()

################################################################################
