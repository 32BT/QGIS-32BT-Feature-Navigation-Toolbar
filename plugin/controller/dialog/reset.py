
from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QDialog

from .samplebox import SampleBox

################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    form, _ = uic.loadUiType(path+'.ui')
    return form

def _int(x, alt=None):
    try: return int(x or 0)
    except (TypeError, ValueError): return alt

################################################################################
### ResetDialog
################################################################################

import sys
_MOD = sys.modules.get(__name__.split('.')[0])
_STR = _MOD.LANGUAGE.STR

_TITLE = _STR("Reset Navigation")
_LABEL = _STR("You have {} features selected for navigation in layer '{}'.")
_CHECK = _STR("Random sample")

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_TITLE)
        self.sampleCheckBox.setText(_CHECK)
        self.sampleCheckBox.toggled.connect(self.sampleCheckBoxToggled)
        self.sampleBox = None

    def sampleCheckBoxToggled(self, state):
        if not self.sampleBox:
            self.sampleBox = SampleBox(self.maxSize)
            self.layout().insertWidget(3, self.sampleBox)
        self.sampleBox.setEnabled(state)

    ########################################################################
    ### Entrypoint
    ########################################################################
    def confirmReset(self, layer):
        self.setLayer(layer)
        if self.exec():
            return self.getSize()

    def setLayer(self, layer):
        self._layer = layer
        name = layer.name()
        size = layer.selectedFeatureCount()
        self.selectionInfo.setText(_LABEL.format(size, name))
        self.maxSize = size

    def getSize(self):
        if self.sampleCheckBox.isChecked():
            return self.sampleBox.getSize()
        else:
            return self.maxSize



