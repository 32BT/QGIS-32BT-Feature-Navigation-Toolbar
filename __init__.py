
class IDENTITY:
    from .identity import PREFIX

class LANGUAGE:
    from .language import String as STR

def classFactory(iface):
    from .plugin import Plugin
    return Plugin(iface)
