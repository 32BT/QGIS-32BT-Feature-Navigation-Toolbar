
from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *


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
### SampleBox
################################################################################

import sys
_MOD = sys.modules.get(__name__.split('.')[0])
_STR = _MOD.LANGUAGE.STR

_TITLE = _STR("Random sample")
_LABEL = _STR("Select or enter the desired samplesize below.")
_SAMPLE_SIZE = _STR("Samplesize:")
_SAMPLE_COUNT = _STR("Count:")

class SampleBox(QWidget, _form()):

    def __init__(self, maxSize=2):
        super().__init__()
        self.setupUi(self)

        self.sampleInfo.setText(_LABEL)
        self.sampleComboLabel.setText(_SAMPLE_SIZE)
        self.sampleCountLabel.setText(_SAMPLE_COUNT)
        validator = self.IntValidator(1, 100, "%")
        self.sampleCombo.lineEdit().setValidator(validator)
        self.sampleCombo.lineEdit().setAlignment(Qt.AlignRight)
        self.sampleCount.setValidator(self.IntValidator())

        self.sampleCombo.currentTextChanged.connect(self.sampleComboChanged)
        self.sampleCombo.lineEdit().editingFinished.connect(self.sampleComboFinished)
        self.sampleCount.textEdited.connect(self.sampleCountChanged)
        self.sampleCount.editingFinished.connect(self.sampleCountFinished)

        self.maxSize = maxSize
        self.setSize(maxSize)

    ########################################################################
    ### Signalhandlers
    ########################################################################

    def sampleComboChanged(self, txt):
        self.controlChanged(self.sampleCombo)

    def sampleComboFinished(self):
        self.setPercentage(self.getPercentage())

    def sampleCountChanged(self):
        self.controlChanged(self.sampleCount)

    def sampleCountFinished(self):
        self.setSize(self.getSize())

    def controlChanged(self, sender):
        # Try round(17 * 50 / 100)
        def _DIV(n, d): return (2*n+d)//(2*d)

        if sender == self.sampleCount:
            n = self.getSize()
            p = _DIV(100 * n, self.maxSize)
            with QSignalBlocker(self.sampleCombo):
                self.setPercentage(p)
        elif sender == self.sampleCombo:
            p = self.getPercentage()
            n = _DIV(self.maxSize * p, 100)
            with QSignalBlocker(self.sampleCount):
                self.setSize(n)

    ########################################################################
    ### Input
    ########################################################################
    '''
    User can either enter a percentage, or a count.
    The signals will ensure update of the sibling control.
    The final value is fetched from the count control.
    '''
    def setPercentage(self, p):
        p = self.limitPercentage(p)
        self.sampleCombo.setCurrentText(str(p)+"%")

    def getPercentage(self):
        try:
            txt = self.sampleCombo.currentText()
            val = int(txt.replace("%", "") or 0)
            return self.limitPercentage(val)
        except Exception as error:
            return 100

    def limitPercentage(self, p):
        return min(max(1, p), 100)

    ########################################################################

    def setSize(self, size):
        size = self.limitSize(size)
        self.sampleCount.setText(str(size))

    def getSize(self):
        try:
            size = int(self.sampleCount.text() or 0)
            return self.limitSize(size)
        except Exception:
            return self.maxSize

    def limitSize(self, size):
        return min(max(2, size), self.maxSize)

    ########################################################################
    ### Validators
    ########################################################################
    '''
    We use validator to ensure digits, and editingFinished to ensure domain.
    State "Intermediate" however, will not trigger editingFinished,
    so we return "Intermediate" as "Acceptable". It does mean that "getSize"
    should be prepared for empty text and domain violations.

    By adding unit, we can use validator for both int, as well as percentage.
    '''
    class IntValidator(QIntValidator):
        def __init__(self, minValue=None, maxValue=None, unit=""):
            super().__init__()
            if minValue is not None: self.setBottom(minValue)
            if maxValue is not None: self.setTop(maxValue)
            self._unit = unit

        def validate(self, txt, pos):
            txt = txt.replace(self._unit, "")
            state, txt, pos = super().validate(txt, pos)
            if state != self.State.Invalid:
                state = self.State.Acceptable
            return state, txt+self._unit, pos



