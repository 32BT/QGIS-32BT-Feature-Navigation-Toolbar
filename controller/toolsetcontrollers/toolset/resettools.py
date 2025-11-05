
from qgis.PyQt.QtCore import *

from .toolset import ToolSet


class ResetTools(ToolSet):
    resetClicked = pyqtSignal()

    def __init__(self, toolBar, iconName="mActionRunSelected"):
        super().__init__(toolBar, {"Reset": iconName })

    def parseAction(self, action):
        self.resetClicked.emit()
        return True
