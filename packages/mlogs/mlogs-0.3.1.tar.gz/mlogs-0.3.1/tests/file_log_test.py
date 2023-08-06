#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 3:26 PM
# @Author  : chenDing
from tests.file_log_test import Lf


if __name__ == '__main__':
    Lf.debug("lalla")
    Lf.info("lalla")
    Lf.warning("lalla")
    Lf.error("lalla")
    Lf.critical("lalla")
    Lf.exception("lalla")
