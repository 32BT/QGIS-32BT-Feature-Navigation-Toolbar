
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
    "SAMPLEDIALOG_TITLE":
        "Custom Sample",
    "SAMPLEDIALOG_LABEL":
        "The full set contains {} features from layer '{}'.",
    "SAMPLEBOX_TITLE":
        "Random sample" })

################################################################################
### SampleDialog
################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.SAMPLEDIALOG_TITLE)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, size, maxSize, layerName):
        self.maxSize = maxSize
        infoLabel = _LABELS.SAMPLEDIALOG_LABEL.format(maxSize, layerName)
        self.infoLabel.setText(infoLabel)
        self.sampleBox = SampleBox(size, self.maxSize)
        self.layout().insertWidget(1, self.sampleBox)
        if self.exec():
            return self.sampleBox.getSize()
