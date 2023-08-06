# -*- coding: utf-8 -*-
import blackblox.dataconfig_defaults as cfg_defaults
from blackblox.bb_log import get_logger


bbcfg = cfg_defaults.default
"""Config: The global configuration object used throughout the library

Initially set to the defaults from `blackblox.dataconfig_defaults` upon import.
The (nested) config values can then be customized using the set_* functions from `blackblox.dataconfig`.  
"""


logger = get_logger("config")
