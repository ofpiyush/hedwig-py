"""
 (@,@)
                _          _
  /\  /\___  __| |_      _(_) __ _
 / /_/ / _ \/ _` \ \ /\ / / |/ _` |
/ __  /  __/ (_| |\ V  V /| | (_| |
\/ /_/ \___|\__,_| \_/\_/ |_|\__, |
                             |___/
"""

__title__ = 'Hedwig Python'
__version__ = '0.0.6'
__author__ = 'Piyush'

# Version synonym
VERSION = __version__

import logging

try:
    # not available in python 2.6
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

# Add NullHandler to prevent logging warnings
logging.getLogger(__name__).addHandler(NullHandler())
