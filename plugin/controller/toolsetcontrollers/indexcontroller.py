
import random, math

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *

from .toolscontroller import ToolsController
from .toolset import IndexTools
from .engine import IndexItems
from ..dialog import SampleDialog
################################################################################
### ItemsMenu Definitions
################################################################################

from .toolset.itemsmenu import ItemsMenu as MENU

################################################################################
### IndexController
################################################################################

class IndexController(ToolsController):
    didSelectFeature = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__(iface, IndexTools(toolBar))
        self._layerItems = None
        self._indexItems = None
        self._tools.indexChanged.connect(self.selectItem)

    ########################################################################
    ### Delegate Actions
    ########################################################################

    def updateMenuAction(self, sender, action, idx):
        if idx == MENU.BUTTON.INDEX:
            enable = self.validateButton()
            return action.setEnabled(enable)
        if idx == MENU.ITEM.INDEX.LOAD_SELECTION:
            enable = self.validateLoadSelection()
            return action.setEnabled(enable)
        if idx == MENU.ITEM.INDEX.SELECT_ALL:
            enabled = self.validateSelectAll()
            return action.setEnabled(enabled)
        if idx == MENU.ITEM.INDEX.SELECT_REMAINING:
            enabled = self.validateSelectAllRemaining()
            return action.setEnabled(enabled)
        if idx == MENU.ITEM.INDEX.SELECT_PRECEDING:
            enabled = self.validateSelectAllPreceding()
            return action.setEnabled(enabled)
        if idx == MENU.ITEM.INDEX.RANDOM_SAMPLE:
            enabled = self.validateRandomSample()
            return action.setEnabled(enabled)

        if idx == MENU.ITEM.INDEX.CLEAR_SAMPLE:
            enabled = self.validateClearSample()
            return action.setEnabled(enabled)
        if idx == MENU.ITEM.INDEX.CUSTOM_SAMPLE:
            enabled = True
            return action.setEnabled(enabled)

    def handleMenuAction(self, sender, action, idx):
        if idx == MENU.ITEM.INDEX.LOAD_SELECTION:
            return self.loadSelection()
        if idx == MENU.ITEM.INDEX.SELECT_ALL:
            return self.selectAll()
        if idx == MENU.ITEM.INDEX.SELECT_REMAINING:
            return self.selectAllRemaining()
        if idx == MENU.ITEM.INDEX.SELECT_PRECEDING:
            return self.selectAllPreceding()

        if idx == MENU.ITEM.INDEX.CLEAR_SAMPLE:
            return self.clearSample()
        if idx < MENU.ITEM.INDEX.CUSTOM_SAMPLE:
            return self.setSample(action.data())
        if idx == MENU.ITEM.INDEX.CUSTOM_SAMPLE:
            if self.askSample():
                sender.setDefaultSampleAction(action)

    ########################################################################
    ### Slots
    ########################################################################
    '''
    self._layerItems are the ids of the original selection
    self._indexItems are the ids actually loaded (which may be a random subset)
    '''
    def validateButton(self):
        return (bool(self._layerItems) or
        self.validateLoadSelection())

    def validateLoadSelection(self):
        layer = self._iface.activeLayer()
        return self.validateLayer(layer)

    def validateSelectAll(self):
        return bool(self._indexItems) and len(self._indexItems) > 0

    def validateSelectAllRemaining(self):
        maxIndex = len(self._indexItems)-1 if self._indexItems else 0
        return 0 < self._tools.index() < maxIndex

    def validateSelectAllPreceding(self):
        maxIndex = len(self._indexItems)-1 if self._indexItems else 0
        return 0 < self._tools.index() < maxIndex

    def validateRandomSample(self):
        return bool(self._layerItems)

    def validateClearSample(self):
        return len(self._indexItems) < len(self._layerItems)

    ########################################################################

    def loadSelection(self):
        layer = self._iface.activeLayer()
        if self.validateLayer(layer):
            self.setLayer(layer)

    def selectAll(self):
        layer = QgsProject.instance().mapLayer(self._layerID)
        if layer: layer.selectByIds(list(self._indexItems))

    def selectAllRemaining(self):
        items = list(self._indexItems)[self._tools.index():]
        layer = QgsProject.instance().mapLayer(self._layerID)
        if layer: layer.selectByIds(items)

    def selectAllPreceding(self):
        items = list(self._indexItems)[:self._tools.index()]
        layer = QgsProject.instance().mapLayer(self._layerID)
        if layer: layer.selectByIds(items)

    def clearSample(self):
        self.setIndexItems(self._layerItems)

    def setSample(self, sampleRatio=100, sampleSize=None):
        if sampleSize is None:
            sampleSize = (sampleRatio * len(self._layerItems)+50)//100
        sampleSize = max(2, sampleSize)
        if sampleSize < len(self._layerItems):
            if sampleSize != len(self._indexItems):
                A = self._layerItems
                A = random.sample(A, k=sampleSize)
                self.setIndexItems(A)

    def askSample(self):
        parent = self._iface.mainWindow()
        size = len(self._indexItems)
        maxSize = len(self._layerItems)
        layerName = self._layer.name()
        size = SampleDialog(parent).askInput(size, maxSize, layerName)
        if size and 2 <= size < maxSize:
            self.setSample(sampleSize=size)
            return True
        return False

    ########################################################################
    ### Layer
    ########################################################################
    '''
    To start process, IndexController requires:
        - a featurelayer with a selection of features
    '''
    def validateLayer(self, layer):
        return (super().validateLayer(layer)
                and layer.isSpatial()
                and hasattr(layer, "getFeature")
                and layer.selectedFeatureCount() > 1)


    def setLayer(self, layer):
        self._layer = layer
        self._layerID = None
        self._layerItems = None
        self._indexItems = None
        self._tools.reset()
        if layer and layer.isValid():
            src = layer.selectedFeatureIds()
            src = list(sorted(src))
            if len(src) > 1:
                self._layerID = layer.id()
                self._layerItems = src
                self.setIndexItems(src)

    def setIndexItems(self, itemList):
        self._indexItems = IndexItems(itemList)
        self._tools.reset(len(self._indexItems)-1)
        self.selectFeature(self._indexItems[0])

    ########################################################################
    ### Actions
    ########################################################################
    '''
    If current index is not in the currently selected features, then a single
    step navigation attempt should first move to the current index, not to
    the next index. Setting the lock, grays out the indexlabel and ensures
    we start again at current index.
    '''
    def updateActions(self):
        layer = self._layer
        if layer:
            idx = self._tools.index()
            fid = self._indexItems.get(idx)
            lock = fid not in layer.selectedFeatureIds()
            self._tools.setIndexLocked(lock)
        super().updateActions()

    '''
    The indextoolset emits an indexChanged signal whenever its index changes.
    The feature selected in self._layer should change accordingly.
    '''
    def indexChanged(self, index=0):
        self.selectItem(index)

    '''
    If index was locked (because the corresponding feature was not in the
    current selection), then instead of an indexChanged signal, we get
    a toolbutton signal.
    '''
    def handleToolsAction(self, action):
        if self._tools.indexLocked():
            index = self._tools.index()
            self.selectItem(index)
        return True

    ########################################################################
    ### Selection
    ########################################################################
    '''
    If index is None or out-of-bounds, then items.get(index) will return None
    If selectFeature receives None, then it will deselect any selection.
    '''
    def selectItem(self, index=None):
        fid = self._indexItems.get(index)
        self.selectFeature(fid)


    def selectFeature(self, fid=None):
        if fid is None:
            # deselect all
            self._layer.removeSelection()
        else:
            # select fid (and deselect previous) then zoom to
            self._layer.selectByIds([fid])
            self.zoomToFeatureID(fid)
        self.didSelectFeature.emit(fid)

    '''
    For userconvenience, other tools are allowed to move the navigation forward.
    The labelcontroller for example will label the currently selected features.
    These features should become part of the history and the next available
    unprocessed item should then be selected.

    This is solved by the selectNextFeature method. This method will keep
    rotating through all unprocessed items until all items are parsed.

    If no more items are available, then items.nextIndex will return None,
    and controller will deselect any selection.
    '''
    def selectNextFeature(self):
        if self._layer:
            # Move selected features to parsed items
            self.parseSelectedFeatures()
            # Get current tool-index
            idx = self.getNextIndex()
            if idx is None:
                self.indexChanged(idx)
            elif self._tools.index() == idx:
                self.indexChanged(idx)
            else:
                # update buttons and emit indexChanged
                self._tools.setIndex(idx)


    def getNextIndex(self):
        # Get current tool-index
        idx = self._tools.index()
        # Select next idx if not locked
        if not self._tools.indexLocked():
            idx = self._indexItems.nextIndex(idx)
        return idx


    def parseSelectedFeatures(self):
        if self._indexItems.parseItems(ids):
            # ids included new items, adjust indextools accordingly
            maxIndex = len(self._indexItems)-1
            idx = self._tools.index()
            idx += maxIndex - self._tools.maxIndex()
            self._tools.setMaxIndex(maxIndex)
            self._tools.setIndex(idx)


    def _parseSelectedFeatures(self):
        cnt = len(self._indexItems)
        ids = self._layer.selectedFeatureIds()
        self._indexItems.parseItems(ids)
        if len(self._indexItems) > cnt:
            # ids included new items, adjust indextools accordingly
            self._tools.setMaxIndex(len(self._indexItems)-1)
            idx = self._tools.index()
            idx += len(self._indexItems)-cnt
            self._tools.setIndex(idx)

    ########################################################################
    ### Zoom
    ########################################################################

    ZOOM_STEP = 250

    def zoomToFeatureID(self, fid):
        f = self._layer.getFeature(fid)
        if f and f.isValid():
            self.zoomToFeature(f)

    def zoomToFeature(self, f):
        b = f.geometry().boundingBox()
        self.zoomToExtent(b)

    def zoomToExtent(self, e):
        mapCanvas = self._iface.mapCanvas()
        s = 1.05 * self._scaleToFit(e)
        n = s / self.ZOOM_STEP
        s = math.ceil(n) * self.ZOOM_STEP
        mapCanvas.zoomByFactor(s/mapCanvas.scale(), e.center())


    def _scaleToFit(self, e):
        mapCanvas = self._iface.mapCanvas()
        s = mapCanvas.scale()
        c = mapCanvas.extent()
        sx = max(1, e.width()) / c.width()
        sy = max(1, e.height()) / c.height()
        return s * max(sx,sy)


    '''
    Following code creates two history extent entries, instead of one.
    mapCanvas.freeze() makes no difference.

    def zoomToExtent(self, e):
        return self._zoomToExtent(e, self.ZOOM_STEP)
        mapCanvas = self._iface.mapCanvas()
        mapCanvas.zoomToFeatureExtent(e)
        n = mapCanvas.scale()/self.ZOOM_STEP
        s = math.ceil(n)*self.ZOOM_STEP
        mapCanvas.zoomScale(s)
    '''
