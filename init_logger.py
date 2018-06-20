#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

LOG_LEVEL = 'DEBUG'
LOF_FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'  # noqa


def init_logger():
    """初始化日志配置"""
    logging.basicConfig(level=LOG_LEVEL, format=LOF_FORMAT)

init_logger()
