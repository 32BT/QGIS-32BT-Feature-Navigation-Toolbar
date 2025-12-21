
import math

from qgis.PyQt.QtCore import *

from .toolscontroller import ToolsController
from .toolset import IndexTools
from .engine import IndexItems


class IndexController(ToolsController):
    didSelectFeature = pyqtSignal(object)

    def __init__(self, iface, toolBar):
        super().__init__(iface, IndexTools(toolBar))
        self._tools.indexChanged.connect(self.selectItem)
        self.updateActions()

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
        self._items = None
        self._tools.reset()
        if layer and layer.isValid():
            src = layer.selectedFeatureIds()
            if len(src) > 1:
                self._items = IndexItems(src)
                self._tools.reset(len(self._items)-1)
                self.selectFeature(self._items[0])

    ########################################################################
    ### Actions
    ########################################################################
    '''
    The indextoolset emits an indexChanged signal whenever its index changes.
    The feature selected in self._layer should change accordingly.
    '''
    def indexChanged(self, index=0):
        self.selectItem(index)

    '''
    If no features are selected, then a single step navigation attempt should
    first move to the current index, not to the next index.
    If IndexTools does not update index due to the lock, then HandleToolsAction
    will be called instead. This will select the current item.
    '''
    def selectedFeaturesChanged(self, layer):
        if self._layer==layer and layer:
            lock = layer.selectedFeatureCount()==0
            self._tools.setIndexLocked(lock)

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
        fid = self._items.get(index)
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
    For userconvenience other tools are allowed to move the navigation forward.
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
            idx = self._items.nextIndex(idx)
        return idx

    def parseSelectedFeatures(self):
        cnt = len(self._items)
        ids = self._layer.selectedFeatureIds()
        self._items.parseItems(ids)
        if len(self._items) > cnt:
            # ids included new items, adjust indextools accordingly
            self._tools.setMaxIndex(len(self._items)-1)
            idx = self._tools.index()
            idx += len(self._items)-cnt
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
        if b.isEmpty(): b.grow(1.)
        self.zoomToExtent(b)

    def zoomToExtent(self, e):
        mapCanvas = self._iface.mapCanvas()
        mapCanvas.zoomToFeatureExtent(e)
        n = mapCanvas.scale()/self.ZOOM_STEP
        s = math.ceil(n)*self.ZOOM_STEP
        mapCanvas.zoomScale(s)
