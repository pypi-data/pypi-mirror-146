import logging

from rqdatac import *
import rqdatac.decorators

from .client import init
from ._version import get_versions

rqdatac.decorators.log = logging.getLogger('dqdata')
__version__ = get_versions()['version']
del get_versions
