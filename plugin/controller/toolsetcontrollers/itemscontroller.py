

from qgis.PyQt.QtCore import *

from .toolscontroller import ToolsController
from .toolset import ResetTools

################################################################################
### ItemsController
################################################################################
'''

'''
class ItemsController(ToolsController):

    def __init__(self, iface, toolBar, icon="mActionRunSelected"):
        super().__init__(iface, ResetTools(toolBar, icon))

    '''
    Delegate is attached directly to menu.
    Updates include the menu-toolbarbutton itself, see ResetTools.updateActions.
    '''
    def setDelegate(self, delegate):
        menu = self._tools.getMenu()
        if hasattr(delegate, "updateMenuAction"):
            menu.updateAction.connect(delegate.updateMenuAction)
        if hasattr(delegate, "handleMenuAction"):
            menu.handleAction.connect(delegate.handleMenuAction)
