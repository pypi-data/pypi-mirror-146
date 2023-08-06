try:
    from importlib_metadata import version
except ModuleNotFoundError:
    from importlib.metadata import version

try:
    __version__ = version("sdd_segmentation")
except:
    __version__ = 'dev'