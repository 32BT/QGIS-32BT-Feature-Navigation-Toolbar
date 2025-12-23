
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
        validator = self.Validator()
        self.sampleCombo.setValidator(validator)
        self.sampleCombo.lineEdit().setValidator(validator)
        self.sampleCount.setValidator(self.IntValidator())

        self.sampleCombo.currentTextChanged.connect(self.sampleComboChanged)
        self.sampleCount.textEdited.connect(self.sampleCountChanged)
        self.sampleCount.editingFinished.connect(self.sampleCountFinished)

        self.maxSize = maxSize
        self.setSize(maxSize)

    def sampleComboChanged(self, txt):
        self.controlChanged(self.sampleCombo)

    def sampleCountChanged(self):
        self.controlChanged(self.sampleCount)

    def sampleCountFinished(self):
        self.setSize(self.getSize())

    def controlChanged(self, sender):
        if sender == self.sampleCount:
            n = self.getSize()
            p = round(100 * n / self.maxSize)
            with QSignalBlocker(self.sampleCombo):
                self.setPercentage(p)
        elif sender == self.sampleCombo:
            p = self.getPercentage()
            n = (p * self.maxSize + 99) // 100
            with QSignalBlocker(self.sampleCount):
                self.setSize(n)


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


