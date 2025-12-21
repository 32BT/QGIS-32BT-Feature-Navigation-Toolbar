
class IDENTITY:
    AUTHOR = '32bt'
    MODULE = 'fnt'
    PREFIX = AUTHOR+'.'+MODULE+'.'

class LANGUAGE:
    from .language import _str as STR

def classFactory(iface):
    from .plugin import Plugin
    return Plugin(iface)
