from .rumbledb import RumbleDBLivyMagic

def load_ipython_extension(ipython):
    ipython.register_magics(RumbleDBLivyMagic)
