

from qgis.core import QgsApplication

_dictionary = None

################################################################################
### _str
################################################################################
'''
'''
class _str(str):
    language = QgsApplication.instance().locale()

    def __new__(cls, txt):
        global _dictionary
        if _dictionary is None:
            _dictionary = Dictionary()
        try:
            key = txt.strip()
            val = _dictionary[key]
            txt = txt.replace(key, val)
            return str.__new__(cls, txt)
        except KeyError:
            # return the input, since we don't know source-language
            return txt

################################################################################
### Library
################################################################################

import os

class Dictionary(dict):
    def __init__(self, lang=None):
        super().__init__()
        lang = lang or QgsApplication.instance().locale()
        path = os.path.dirname(__file__)
        path = os.path.join(path, str(lang).lower()+'.txt')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                rows = list(f)
            rows = [row.strip() for row in rows]
            rows = [row for row in rows if row and row[0] != '#']
            self.update(zip(rows[0::2],rows[1::2]))

