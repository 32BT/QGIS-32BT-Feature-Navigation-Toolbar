

class IDENTITY:
    AUTHOR = '32bt'
    MODULE = 'fnt'
    PREFIX = AUTHOR+'.'+MODULE+'.'


def classFactory(iface):
    from .plugin import Plugin
    return Plugin(iface)
