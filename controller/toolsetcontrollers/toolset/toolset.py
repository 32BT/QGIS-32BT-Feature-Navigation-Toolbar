
import os, sys

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *

################################################################################
import sys
_MOD = sys.modules.get(__name__.split('.')[0])
_str = _MOD.language._str

def _objectname(name):
    return _MOD.IDENTITY.PREFIX+name
################################################################################


class ToolSet(QObject):
    actionTriggered = pyqtSignal(object)

    def __init__(self, toolBar, info={}):
        super().__init__()
        self._toolBar = toolBar
        self._actions = []
        self._prepare(toolBar, info)

    ########################################################################
    ### Prepare
    ########################################################################
    def _prepare(self, toolBar, info={}):
        self._actions = self._prepareActions(info)
        self._prepareToolBar(toolBar, self._actions)

    '''
    Create actions from a dictionary with actionName, iconName pairs.
    '''
    def _prepareActions(self, info={}):
        actions = []
        for name, icon in info.items():
            action = self._prepareAction(icon, name)
            actions.append(action)
        return actions

    def _prepareAction(self, icon, name, proc=None):
        if isinstance(icon, str):
            icon = self._load_icon(icon)
        action = QAction(icon, _str(name))
        action.setObjectName(_objectname(name))
        action.setEnabled(False)
        if proc: action.triggered.connect(proc)
        return action


    def _load_icon(self, path):
        if os.path.exists(path):
            icon = QIcon(os.path.relpath(path))
        else:
            name = os.path.split(path)[-1]
            name = self._icon_name(name)
            path = self._icon_path(name)
            icon = QIcon(os.path.relpath(path))
        if icon.isNull():
            icon = QgsApplication.getThemeIcon(name)
        return icon

    def _icon_name(self, name):
        name = name.replace(' ','')
        if not name.startswith('mAction'):
            name = 'mAction'+name
        name, ext = os.path.splitext(name)
        if not ext: ext = '.svg'
        return name+ext

    def _icon_path(self, name):
        path = __file__
        path = os.path.split(path)[0]
        path = os.path.join(path, "icons")
        path = os.path.join(path, name)
        return path


    def _prepareToolBar(self, toolBar, actions):
        # Add a separator if there are other actions in toolBar
        if toolBar.actions():
            toolBar.addSeparator()
        toolBar.addActions(actions)
        toolBar.actionTriggered.connect(self.parseToolBarAction)


    def replaceActions(self, info={}):
        beforeAction = self.removeActions()
        self._actions = self._prepareActions(info)
        for action in self._actions:
            self._toolBar.insertAction(beforeAction, action)

    def removeActions(self):
        beforeAction = None
        if self._actions:
            index = self._toolBar.actions().index(self._actions[0])
            for action in self._actions:
                self._toolBar.removeAction(action)
            if index < len(self._toolBar.actions()):
                beforeAction = self._toolBar.actions()[index]
            self._actions = None
        return beforeAction

    ########################################################################
    ### Update
    ########################################################################
    '''
    Controller needs to be able to activate actions in response to signals and
    statechanges.
    '''
    def updateActions(self):
        pass

    def setEnabled(self, enabled=True, index=None):
        if index is None:
            for action in self._actions:
                action.setEnabled(enabled)
        else:
            self._actions[index].setEnabled(enabled)

    def enableActions(self, enable=True):
        for action in self._actions:
            action.setEnabled(enable)

    def enableAction(self, index, enable=True):
        self._actions[index].setEnabled(enable)

    ########################################################################
    ### ToolBar Action Triggered
    ########################################################################
    '''
    ToolSet is a subset of actions in a ToolBar.
    If incoming action belongs to our subset -> parse action.
    '''
    def parseToolBarAction(self, action):
        if action in self._actions:
            if self.parseAction(action):
                self.actionTriggered.emit(action)

    '''
    Parse action allows ToolSet to adjust internal state and possibly emit
    a specific signal. Return True to (also) emit the actionTriggered signal
    after parsing action.

    From here:
        ResetTools emits ResetClicked
        IndexTools will update index and buttons, and then emits indexChanged.
        LabelTools extracts labelname from action, and then emits labelClicked
        with that name.
    '''
    def parseAction(self, action):
        # e.g.: self.labelClicked.emit(action.name())
        return True


