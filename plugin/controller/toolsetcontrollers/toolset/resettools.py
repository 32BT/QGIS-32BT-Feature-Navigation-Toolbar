
from qgis.PyQt.QtCore import *

from .toolset import ToolSet


class ResetTools(ToolSet):
    resetClicked = pyqtSignal()

    '''
    Initialize with run-selected icon.
    This uses the custom run-selected icon in the icons folder.
    The custom icon is a yellow square with a *blue* play button, not
    a green button. By using the default name however, the initializing
    process will alternatively try the default icon, if, for whatever reason,
    the custom icon is not reachable.
    '''
    def __init__(self, toolBar, iconName="mActionRunSelected"):
        super().__init__(toolBar, {"Reset": iconName })

    def parseAction(self, action):
        self.resetClicked.emit()
        return True
