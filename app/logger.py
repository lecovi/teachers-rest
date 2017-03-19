# -*- coding: utf-8 -*-
"""
    logger
    ~~~~~~

    This is the logger configuration module for Teacher's REST application.

    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña.
    :license: GPL v3.0, see LICENSE for more details.

"""
# Standard lib imports
import logging.handlers
import time
import os
import sys
# Third Party imports
from rainbow_logging_handler import RainbowLoggingHandler
# BITSON imports
from config import Config

console_logger = logging.getLogger('trest')
console_logger.setLevel(logging.DEBUG)

console_handler = RainbowLoggingHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(fmt="%(message)s"))

console_logger.addHandler(console_handler)

log_format = "".join(
    ["[%(asctime)s] %(name)20s - %(levelname)8s: ",
     "%(threadName)15s-%(funcName)15s() - %(message)s"]
)
formatter = logging.Formatter(fmt=log_format)
# Format UTC Time
formatter.converter = time.gmtime

if not os.path.isdir(Config.LOG_FOLDER):
    os.mkdir(Config.LOG_FOLDER)

logfile = os.path.join(Config.LOG_FOLDER,
                       '{}.log'.format(Config.PROJECT_NAME))

file_handler = logging.handlers.RotatingFileHandler(filename=logfile,
                                                    maxBytes=10e6,
                                                    backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
