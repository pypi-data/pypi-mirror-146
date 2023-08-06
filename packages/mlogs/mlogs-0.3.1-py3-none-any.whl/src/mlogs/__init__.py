#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 10:39 AM
# @Author  : chenDing
from pathlib import Path
import os
import sys

notifiers_path = os.path.join(Path(os.path.abspath(__file__)).parent, "third_party", "notifiers")
# print(f"notifiers_path: {notifiers_path}")
sys.path.append(notifiers_path)

from .base_logger import logger, BaseLogger
from .mlogger import MLogger
from .adapt_history_logger import AdaptHistoryLogger
from .flie_logger import FileLogger
from .stdout_logger import StdoutLogger

__title__ = 'mlogs'
__authors__ = 'caturbhuja das'
__license__ = 'Apache v2.0'
__copyright__ = 'Copyright 2022 caturbhuja das'
__version__ = "0.3.0"
__version_info__ = tuple(int(i) for i in __version__.split('.'))

__all__ = [
    'BaseLogger', 'MLogger', 'AdaptHistoryLogger',
    'FileLogger', 'StdoutLogger', 'logger', '__title__', '__authors__',
    '__license__', '__copyright__', '__version__', '__version_info__',
]
