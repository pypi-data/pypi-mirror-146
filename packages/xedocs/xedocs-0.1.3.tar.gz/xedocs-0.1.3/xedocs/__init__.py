"""Top-level package for xedocs."""

__author__ = """Yossi Mosbacher"""
__email__ = "joe.mosbacher@gmail.com"
__version__ = "0.1.3"

from ._settings import settings
from ._frames import frames
from . import schemas
from .schemas import *
from .utils import *
from .xedocs import *
from .api import api_client, api_token