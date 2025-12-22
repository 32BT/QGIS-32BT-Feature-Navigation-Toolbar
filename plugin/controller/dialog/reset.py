
from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QDialog


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
_SELECT_INFO = _STR("You have {} features selected for navigation in layer '{}'.")
_SAMPLE_BOX = _STR("Random sample")
_SAMPLE_INFO = _STR("Select or enter the desired samplesize below.")
_SAMPLE_SIZE = _STR("Samplesize:")
_SAMPLE_COUNT = _STR("Count:")

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_TITLE)
        self.sampleBox.setTitle(_SAMPLE_BOX)
        self.sampleInfo.setText(_SAMPLE_INFO)
        self.sampleComboLabel.setText(_SAMPLE_SIZE)
        self.sampleCountLabel.setText(_SAMPLE_COUNT)
        validator = self.Validator()
        self.sampleCombo.setValidator(validator)
        self.sampleCombo.lineEdit().setValidator(validator)
        self.sampleCount.setValidator(self.IntValidator())

        self.sampleCombo.currentTextChanged.connect(self.sampleComboChanged)
        self.sampleCount.textEdited.connect(self.sampleCountChanged)
        self.sampleCount.editingFinished.connect(self.sampleCountFinished)


    def sampleComboChanged(self, txt):
        self.controlChanged(self.sampleCombo)

    def sampleCountChanged(self):
        self.controlChanged(self.sampleCount)

    def sampleCountFinished(self):
        self.setSize(self.getSize())

    def controlChanged(self, sender):
        maxSize = self._layer.selectedFeatureCount()
        if sender == self.sampleCount:
            n = self.getSize()
            p = round(100 * n / self.maxSize())
            with QSignalBlocker(self.sampleCombo):
                self.setPercentage(p)
        elif sender == self.sampleCombo:
            p = self.getPercentage()
            n = (p * self.maxSize() + 99) // 100
            with QSignalBlocker(self.sampleCount):
                self.setSize(n)



    def confirmReset(self, layer):
        size = self.setLayer(layer)
        self.setSize(size)
        if self.exec():
            return self.getSize()

    def setLayer(self, layer):
        self._layer = layer
        name = layer.name()
        size = layer.selectedFeatureCount()
        self.selectionInfo.setText(_SELECT_INFO.format(size, name))
        self.sampleCount.setValidator(self.IntValidator(2, size))
        return size

    def altKeyActive(self):
        modifiers = QgsApplication.instance().keyboardModifiers()
        return bool(modifiers & Qt.AltModifier)

    def getPercentage(self):
        try:
            txt = self.sampleCombo.currentText()
            return int(txt.replace("%", "") or 0)
        except Exception as error:
            return 100

    def setPercentage(self, p):
        self.sampleCombo.setCurrentText(str(p)+"%")

    def setSize(self, size):
        size = self.limitSize(size)
        self.sampleCount.setText(str(size))

    def getSize(self):
        if not self.sampleBox.isChecked():
            return self.maxSize()
        try:
            size = int(self.sampleCount.text() or 0)
            return self.limitSize(size)
        except Exception:
            return self.maxSize()

    def limitSize(self, size):
        return min(max(2, size), self.maxSize())

    def maxSize(self):
        maxSize = 2
        if hasattr(self, '_layer'):
            if self._layer and self._layer.isValid():
                maxSize = self._layer.selectedFeatureCount()
        return maxSize

    ########################################################################
    ### Validators
    ########################################################################
    '''
    Returning state "Intermediate" will not trigger editingFinished,
    so we allow empty text as "Acceptable". It does mean that "getSize"
    should be prepared for empty text.
    '''
    class IntValidator(QIntValidator):
        def validate(self, txt, pos):
            state, txt, pos = super().validate(txt, pos)
            if state != self.State.Invalid:
                state = self.State.Acceptable
            return state, txt, pos


    class Validator(QValidator):
        def validate(self, txt, pos):
            if not txt:
                state = self.State.Intermediate
            elif self.acceptable(txt):
                state = self.State.Acceptable
            else:
                state = self.State.Invalid
            return (state, txt, pos)

        def acceptable(self, txt):
            try: return 0 < int(txt.replace("%","")) <= 100
            except Exception: return False


