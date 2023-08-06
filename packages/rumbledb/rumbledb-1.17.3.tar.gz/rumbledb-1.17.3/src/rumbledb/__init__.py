from .rumbledb import RumbleDBServerMagic

def load_ipython_extension(ipython):
    ipython.register_magics(RumbleDBServerMagic)
