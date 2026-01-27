

'''
Array with history
'''

class IndexItems:
    def __init__(self, items):
        self._pastItems = []
        self._nextItems = list(items)

    def pastItems(self):
        return self._pastItems

    def nextItems(self):
        return self._nextItems

    def __len__(self):
        return len(self._pastItems)+len(self._nextItems)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx < 0: idx += len(self)
            if 0 <= idx < len(self._pastItems):
                return self._pastItems[idx]
            idx -= len(self._pastItems)
            if 0 <= idx < len(self._nextItems):
                return self._nextItems[idx]
            raise IndexError
        raise TypeError


    def get(self, idx, alt=None):
        try:
            return self[idx]
        except (IndexError, TypeError):
            return alt


    def findIndex(self, fid):
        try: return self._pastItems.index(fid)
        except ValueError:
            try: return len(self._pastItems)+self._nextItems.index(fid)
            except ValueError: pass


    def nextIndex(self, idx):
        idx += 1
        # Rotate over unprocessed items
        if len(self._nextItems):
            if idx < len(self._pastItems):
                idx = len(self._pastItems)
            if idx > len(self)-1:
                idx = len(self._pastItems)
        if idx < len(self):
            return idx
        return None

    def parseItems(self, items):
        return sum(self.parseItem(item) for item in items)

    def parseItem(self, item):
        if item not in self._pastItems:
            self._pastItems.append(item)
            if item not in self._nextItems: return True
            self._nextItems.remove(item)
        return False
