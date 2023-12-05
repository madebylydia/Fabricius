from importlib.metadata import distribution as __dist

__version__ = __dist("fabricius").version
__author__ = __dist("fabricius").metadata["Author"]
