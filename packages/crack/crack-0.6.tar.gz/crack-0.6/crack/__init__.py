# -*- coding: utf-8 -*-
# @author: leesoar

"""crack"""

import sys

from crack.font import Font
from crack.util import *
try:
    from pysodium import *
# except ValueError:
except Exception:
    # if error -> need install libsodium
    pass


__version__ = "0.6"

if sys.version_info >= (3, 6):
    from secrets import *