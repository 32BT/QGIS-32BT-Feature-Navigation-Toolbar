
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

################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "RESETDIALOG_TITLE":
        "Reset Navigation",
    "RESETDIALOG_LABEL":
        "You have {} features selected for navigation in layer '{}'.",
    "SAMPLEBOX_TITLE":
        "Random sample" })

################################################################################
### ResetDialog
################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.RESETDIALOG_TITLE)
        self.sampleCheckBox.setText(_LABELS.SAMPLEBOX_TITLE)
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
        label = _LABELS.RESETDIALOG_LABEL.format(size, name)
        self.selectionInfo.setText(label)
        self.maxSize = size

    def getSize(self):
        if self.sampleCheckBox.isChecked():
            return self.sampleBox.getSize()
        else:
            return self.maxSize



