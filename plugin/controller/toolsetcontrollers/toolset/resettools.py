
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from .toolset import ToolSet
from .itemsmenu import ItemsMenu


class ResetTools(ToolSet):
    resetClicked = pyqtSignal()

    def __init__(self, toolBar, iconName="mActionRunSelected"):
        super().__init__(toolBar)

        '''
        QToolButton with menu does not unraise properly after showing the menu,
        plus the tiny disclosure triangle is not particularely helpful for
        indicating a major InstantPopup.
        So we just build a full actionchain ourselves.
        '''
        self._menu = ItemsMenu()
        self._menu.aboutToHide.connect(self.menuDidFinish)

        self._action = QAction()
        self._action.setIcon(self._load_icon(iconName))
        self._action.triggered.connect(self.showMenu)
        self._actions.append(self._action)

        self._button = QToolButton()
        self._button.setDefaultAction(self._action)
        toolBar.addWidget(self._button)

    ########################################################################

    def getMenu(self):
        return self._menu

    def getAction(self):
        return self._action

    def getButton(self):
        return self._button

    # Triggered by selectionChanged signal via ItemsController
    def updateActions(self):
        print('goto delegate')
        # Allow delegate to solve the action validation
        self._menu.updateAction.emit(self, self._action, self._menu.BUTTON.INDEX)

    def showMenu(self, action):
        button = self._button
        button.setDown(True)
        x, y = 0, button.frameSize().height()
        self._menu.popup(button.mapToGlobal(QPoint(x,y)))
        return True

    def menuDidFinish(self):
        self._button.setDown(False)

