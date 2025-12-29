
class IDENTITY:
    from .identity import PREFIX

class LANGUAGE:
    from .language import LABELS

def classFactory(iface):
    from .plugin import Plugin
    return Plugin(iface)
