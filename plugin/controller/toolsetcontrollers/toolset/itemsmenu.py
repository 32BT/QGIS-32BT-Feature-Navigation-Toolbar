

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *


################################################################################
### Language
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS({
    "INDEXMENU_TITLE": "Selectionmenu",
    "INDEXMENU_ITEM1": "Load Selection",
    "INDEXMENU_ITEM2": "Select All Items",
    "INDEXMENU_ITEM3": "Select All Remaining Items",
    "INDEXMENU_ITEM4": "Select All Preceding Items",
    "SAMPLEMENU_TITLE": "Random Sample",
    "SAMPLEMENU_ITEM1": "Clear Sample",
    "SAMPLEMENU_ITEM2": "Custom..."})

################################################################################
### Sample Submenu
################################################################################

class SampleMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(_LABELS.SAMPLEMENU_TITLE, parent)
        action = self.addAction(_LABELS.SAMPLEMENU_ITEM1)
        action = self.addSeparator()
        for n in (5, 10, 20, 25, 33, 50):
            action = self.addAction(f"{n}%")
            action.setData(n)
        action = self.addAction(_LABELS.SAMPLEMENU_ITEM2)

################################################################################
### ItemsMenu
################################################################################

class ItemsMenu(QMenu):

    ########################################################################
    ### Definities
    ########################################################################

    class BUTTON:
        INDEX                = -1
    class ITEM:
        class INDEX:
            LOAD_SELECTION   = 0
            SEPARATOR_1      = 1
            SELECT_ALL       = 2
            SELECT_REMAINING = 3
            SELECT_PRECEDING = 4
            SEPARATOR_2      = 5
            RANDOM_SAMPLE    = 6
            CLEAR_SAMPLE     = 7
            SEPARATOR_3      = 8
            SAMPLE_5         = 9
            SAMPLE_10        = 10
            SAMPLE_20        = 11
            SAMPLE_25        = 12
            SAMPLE_33        = 13
            SAMPLE_50        = 14
            CUSTOM_SAMPLE    = 15

    ########################################################################

    updateAction = pyqtSignal(object, object, object)
    handleAction = pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super().__init__(_LABELS.INDEXMENU_TITLE, parent)
        action = self.addAction(_LABELS.INDEXMENU_ITEM1)
        action = self.addSeparator()
        action = self.addAction(_LABELS.INDEXMENU_ITEM2)
        action = self.addAction(_LABELS.INDEXMENU_ITEM3)
        action = self.addAction(_LABELS.INDEXMENU_ITEM4)
        action = self.addSeparator()

        self._sampleMenu = SampleMenu()
        self.addMenu(self._sampleMenu)

        self.aboutToShow.connect(self.updateActions)
        self.triggered.connect(self.actionTriggered)

    ########################################################################

    def updateActions(self):
        actions = self.actions()
        for idx, action in enumerate(actions):
            self.emitUpdate(action, idx)
        # If RandomSampleItem is available, then also update sampleActions
        if action.isEnabled():
            self.updateSampleActions()

    def updateSampleActions(self):
        offset = self.ITEM.INDEX.CLEAR_SAMPLE
        actions = self._sampleMenu.actions()
        for idx, action in enumerate(actions):
            self.emitUpdate(action, offset+idx)

    def actionTriggered(self, action):
        actions = self.actions() + self._sampleMenu.actions()
        idx = actions.index(action)
        self.emitAction(action, idx)
        # Update sampleMenu to reflect an active sampleset if applicable
        if action in self._sampleMenu.actions()[1:-1]:
            self.setDefaultSampleAction(action)
        elif action == self._sampleMenu.actions()[0]:
            self.setDefaultSampleAction(None)

    def setDefaultSampleAction(self, action):
        self._sampleMenu.setDefaultAction(action)

    ########################################################################
    def emitUpdate(self, action, idx):
        self.updateAction.emit(self, action, idx)

    def emitAction(self, action, idx):
        self.handleAction.emit(self, action, idx)
    ########################################################################





