

from qgis.PyQt.QtWidgets import *


################################################################################
### ResetDialog
################################################################################
'''
The pattern for one of our dialogs would normally look like this:

    SomeDialog(parent).askParameter(currentValue)

Based on QDialog it would look somewhat like so:

    class SomeDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent=parent)
            <more setup>

        def askParameter(self, currentValue):
            self.setValue(currentValue)
            if self.exec():
                return self.getValue()

The ResetDialog however, is a simple confirmation dialog and can use one of
the simple convenience dialogclasses. Even so, we maintain the same pattern.
'''

class ResetDialog:
    def __init__(self, parent):
        self._parent = parent

    def confirmReset(self, old_layer, new_layer=None):
        parent = self._parent
        title = self.prepareConfirmResetTitle()
        label = self.prepareConfirmResetLabel(old_layer, new_layer)
        buttons = QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok
        defaultButton = QMessageBox.StandardButton.Cancel
        result = QMessageBox.warning(parent, title, label, buttons, defaultButton)
        return result == QMessageBox.StandardButton.Ok

    def prepareConfirmResetTitle(self):
        return "Reset Navigation"

    def prepareConfirmResetLabel(self, old_layer, new_layer=None):
        text = "Navigation is currently set to layer '{}'.\n".format(old_layer.name())
        text += "Do you want to reset to "
        if old_layer == new_layer:
            text += "the new selection?"
        else:
            text += "layer '{}'?".format(new_layer.name())
        return text

