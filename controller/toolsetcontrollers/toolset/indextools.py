
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *


from .toolset import ToolSet


class IndexTools(ToolSet):
    indexChanged = pyqtSignal(object)

    def __init__(self, toolBar):
        super().__init__(toolBar, {
            "First": "mActionDoubleArrowLeft.svg",
            "Previous": "mActionArrowLeft.svg",
            "Next": "mActionArrowRight.svg",
            "Last": "mActionDoubleArrowRight.svg"})
        self.reset()


    # Add a label between indexbuttons
    def _prepareToolBar(self, toolBar, actions):
        super()._prepareToolBar(toolBar, actions)
        self._label = QLabel()
        toolBar.insertWidget(actions[-2], self._label)

    ########################################################################
    ### Reset
    ########################################################################

    def reset(self, maxIndex=0, hasPages=False):
        self._index = 0
        self._indexLocked = False
        self._minIndex = 0
        self._maxIndex = max(0, maxIndex)
        self._hasPages = hasPages
        self.updateActions()

    ########################################################################
    ### Update
    ########################################################################

    def updateActions(self):
        hasPages = self._hasPages
        enableBack = self._minIndex is None or self._index > self._minIndex
        enableNext = self._maxIndex is None or self._index < self._maxIndex
        self._actions[0].setEnabled(enableBack)
        self._actions[1].setEnabled(enableBack)
        self._actions[2].setEnabled(enableNext or hasPages)
        self._actions[3].setEnabled(enableNext)
        self.updateLabel()

    def updateLabel(self):
        txt = ""
        if self._minIndex != self._maxIndex:
            txt = str(self._index+1)
            if self._maxIndex is not None:
                txt += "/"+str(self._maxIndex+1)
                if self._hasPages:
                    txt += "+"
        self._label.setText(txt)
        self._label.setEnabled(not self._indexLocked)

    ########################################################################
    ### Navigation
    ########################################################################
    '''
    A double arrow technically means "next page", therefore this method
    attempts to jump beyond the index limits. The index will be limited
    appropriately by the setIndex method.

    Index may be locked. This will block a single step navigation attempt, and
    will trigger the toolsAction signal instead. This mechanism is used by
    the controller in case the current item is deselected.
    If there is no selection, then navigation should continue by reselecting
    the current index, not by moving to the next/prev item. Jumping a full page
    on the other hand, is always allowed, and will reset the lock.
    '''
    def parseAction(self, action):
        if self._actions[0] == action:
            self._indexLocked = False
            self.moveToPreviousPage()
        elif self._actions[1] == action:
            self.moveToPreviousItem()
        elif self._actions[2] == action:
            self.moveToNextItem()
        elif self._actions[3] == action:
            self._indexLocked = False
            self.moveToNextPage()
        # If index is locked, trigger toolsAction instead
        return self._indexLocked


    def moveToPreviousPage(self):
        return self.moveToPrevPage()

    def moveToPreviousItem(self):
        return self.moveToPrevItem()

    def moveToPrevPage(self):
        return self.setIndex(self._minIndex-1)

    def moveToPrevItem(self):
        return self.setIndex(self._index-1)

    def moveToNextItem(self):
        return self.setIndex(self._index+1)

    def moveToNextPage(self):
        return self.setIndex(self._maxIndex+1)

    ########################################################################
    ### Index
    ########################################################################
    #TODO if index is len(self) then feedback for no selection
    #(gray out label possibly showing --/100)

    def indexLocked(self):
        return self._indexLocked

    def setIndexLocked(self, lock=True):
        self._indexLocked = lock


    def index(self):
        return self._index

    def setIndex(self, index):
        index = self.limitIndex(index)
        if self._index != index:
            if not self._indexLocked:
                self._index = index
                self.updateActions()
                self.indexChanged.emit(index)
                return True
        return False


    def setMinIndex(self, index):
        if self._minIndex != index:
            self._minIndex = index
            self.updateActions()

    def setMaxIndex(self, index):
        if self._maxIndex != index:
            self._maxIndex = index
            self._index = self.limitIndex(self._index)
            self.updateActions()

    def setPaging(self, paging):
        if self._hasPages != paging:
            self._hasPages = paging
            self._index = self.limitIndex(self._index)
            self.updateActions()

    def limitIndex(self, index):
        minIndex = self._minIndex
        maxIndex = self._maxIndex + self._hasPages
        return min(max(minIndex, index), maxIndex)
