#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 3:27 PM
# @Author  : chenDing
from typing import Optional
from .stdout_logger import StdoutLogger


class AdaptHistoryLogger(StdoutLogger):
    """兼容历史日志"""

    def __init__(self, config: Optional[dict] = None, level: Optional[str] = None, *args, **kwargs):
        """
        :param config:  loguru 配置
        :param level:  指定日志 级别
        """
        super().__init__(config, level, *args, **kwargs)

    def debug(self, trace_id, topic, msg):
        self._logger.opt(colors=True).bind(call_info=self._call_info()).debug(self._format_args(msg, trace_id, topic))

    def info(self, trace_id, topic, msg):
        self._logger.opt(colors=True).bind(call_info=self._call_info()).info(self._format_args(msg, trace_id, topic))

    def warning(self, trace_id, topic, msg):
        self._logger.opt(colors=True).bind(call_info=self._call_info()).warning(
            self._format_args(msg, trace_id, topic))

    def error(self, trace_id, topic, msg):
        self._logger.opt(colors=True).bind(call_info=self._call_info()).error(self._format_args(msg, trace_id, topic))

    def critical(self, trace_id, topic, msg):
        self._logger.opt(colors=True).bind(call_info=self._call_info()).critical(
            self._format_args(msg, trace_id, topic))

    def exception(self, trace_id, topic, msg):
        self._logger.opt(exception=True, colors=True).bind(call_info=self._call_info()).exception(
            self._format_args(msg, trace_id, topic))
