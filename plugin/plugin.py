

################################################################################
### Plugin Main
################################################################################
'''
Note that a NavigationController merely manages a set of actions on a toolbar.
A toolbar may contain additional actions managed by other controllers.
Therefore, toolbar is supplied separately to the controller.
'''

from .controller import ToolBar
from .controller import Controller

class Plugin:
    def __init__(self, iface):
        self._iface = iface

    def initGui(self):
        self._toolBar = ToolBar(self._iface)
        self._controller = Controller(self._iface, self._toolBar)

    def unload(self):
        self._controller = None
        self._toolBar = None

################################################################################
