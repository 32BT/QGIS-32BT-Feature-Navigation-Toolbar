
from qgis.PyQt.QtCore import *
from .layercontroller import LayerController

################################################################################
### ToolsController
################################################################################
'''
ToolsController is a LayerController with a toolset.
It's the baseclass for controlling a toolset with the plumbing to update
the tools as necessary. It responds to layerselection changes and allows
toolsets to update accordingly.

Both the ResetController and IndexController are based on this class.
'''

class ToolsController(LayerController):
    didHandleToolsAction = pyqtSignal(object)

    def __init__(self, iface, toolSet):
        super().__init__(iface)
        self._tools = toolSet
        self._tools.actionTriggered.connect(self.toolsActionTriggered)

    ########################################################################
    '''
    The Selection class will trigger a selectionChanged signal when:
        1. The active layer in the ToC changes
        2. The selection of features on the active layer changes
    '''
    def selectionChanged(self, layer):
        self.updateActions()

    ########################################################################

    # Override setLayer to also include tools update
    def setLayer(self, layer):
        super().setLayer(layer)
        self.updateActions()

    def updateActions(self):
        self._tools.updateActions()

    ########################################################################
    '''
    The actions triggered by a ToolBar are handled by the respective ToolSets.
    They will handle the action for internal state, and then emit a signal:
    '''
    def toolsActionTriggered(self, action):
        if self.handleToolsAction(action):
            self.didHandleToolsAction.emit(action)

    def handleToolsAction(self, action):
        return True

    ########################################################################
