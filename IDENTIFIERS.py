

'''
    import sys

    @classmethod
    def _prefix_name(cls, name):
        mod = cls.__module__.split('.')[0]
        mod = sys.modules.get(mod)
        return mod.IDENTIFIERS.PREFIX + name
'''

AUTHOR = '32bt'
MODULE = 'fnt'
PREFIX = AUTHOR+'.'+MODULE+'.'
