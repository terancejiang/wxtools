#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""

import sys
import logging
from logging.handlers import RotatingFileHandler

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def setup_logger(name, log_file=None, log_level='INFO'):
    log_level_name = log_level
    log_level = LOG_LEVELS.get(log_level_name.upper(), logging.INFO)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler and set level to debug
    if log_file is not None:
        file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Create a console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    return logger
