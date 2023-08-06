# Will be imported instead of pygame to hide the pygame welcome message

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
del os

from pygame import *
from pygame import gfxdraw, display