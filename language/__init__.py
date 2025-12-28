

from qgis.core import QgsApplication


################################################################################
### Labels
################################################################################
'''
For translated labels by reference:
    _LABELS = LABELS(...)
    _LABELS.CUSTOM_LABEL1

For direct translation by text:
    _LABELS = LABELS(...)
    translated_label = _LABELS("Custom Label 1")

'''
import os, json

class LABELS(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().update(self.loadLanguage() or {})

    def __call__(self, k):
        return self.__getattr__(k) or k or ""

    def __getattr__(self, k):
        v = self.get(k)
        if isinstance(v, list):
            v = '\n'.join(v)
        return v or ""

    @classmethod
    def loadLanguage(cls, lang=None):
        lang = lang or QgsApplication.instance().locale()
        path = os.path.dirname(__file__)
        path = os.path.join(path, str(lang).lower()+'.json')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return json.loads(f.read())
