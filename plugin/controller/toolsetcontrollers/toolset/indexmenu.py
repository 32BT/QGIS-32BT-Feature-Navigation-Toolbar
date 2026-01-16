
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *


import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS({
    "INDEXMENU_ITEM1": "Load Selection",
    "INDEXMENU_ITEM2": "Select All Items",
    "INDEXMENU_ITEM3": "Select All Remaining Items",
    "INDEXMENU_ITEM4": "Select All Past Items",
    "SAMPLEMENU_TITLE": "Random Sample",
    "SAMPLEMENU_ITEM1": "Clear Sample",
    "SAMPLEMENU_ITEM2": "Custom..."})


class SampleMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(_LABELS.SAMPLEMENU_TITLE, parent)
        action = self.addAction(_LABELS.SAMPLEMENU_ITEM1)
        action = self.addSeparator()
        for n in (5, 10, 25, 33, 50):
            action = self.addAction(f"{n}%")
        action = self.addAction(_LABELS.SAMPLEMENU_ITEM2)


class IndexMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        action = self.addAction(_LABELS.INDEXMENU_ITEM1)
        action = self.addSeparator()
        action = self.addAction(_LABELS.INDEXMENU_ITEM2)
        action = self.addAction(_LABELS.INDEXMENU_ITEM3)
        action = self.addAction(_LABELS.INDEXMENU_ITEM4)
        action = self.addSeparator()

        self._sampleMenu = SampleMenu()
        self.addMenu(self._sampleMenu)





