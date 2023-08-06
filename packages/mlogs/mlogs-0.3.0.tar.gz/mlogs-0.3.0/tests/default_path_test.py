#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/13 3:13 PM
# @Author  : chenDing
"""
测试在不添加路径时，日志所在位置
预期：自动生成的日志位置，在日志初始化文件平行的目录下。
"""

from mlogs import MLogger
L = MLogger()
L.info("nice")
L.error("nice")
L.warning("nice")

