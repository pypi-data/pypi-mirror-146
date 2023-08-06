#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: xl
@file: conf.py
@time: 2021/08/09
@contact:
@site:
@software: PyCharm
"""
import os

import attrdict
from dotenv import load_dotenv
from loguru import logger

load_dotenv(verbose=True)

METRICS_AGENT_HOST = os.environ.get('METRICS_AGENT_HOST', 'http://127.0.0.1:10039')
METRICS_APP_NAME = os.environ.get('METRICS_APP_NAME', os.environ.get('MY_PRODUCT_NAME', 'service-monitor'))
METRICS_SERVICE_NAME = os.environ.get('METRICS_SERVICE_NAME', os.environ.get('MY_PROJECT_NAME', 'service-monitor-test'))
METRICS_APP_VERSION = os.environ.get('METRICS_APP_VERSION', os.environ.get('MY_VERSION_NAME', 'test'))
METRICS_SKIP_1ST_PERIOD = os.environ.get('METRICS_SKIP_1ST_PERIOD', 'False')
METRICS_STEP = os.environ.get('METRICS_STEP', '60')

CONF = attrdict.AttrDict({
    "METRICS_AGENT_HOST": METRICS_AGENT_HOST,
    "METRICS_APP_NAME": METRICS_APP_NAME,
    'METRICS_SERVICE_NAME': METRICS_SERVICE_NAME,
    'METRICS_APP_VERSION': METRICS_APP_VERSION,
    'METRICS_SKIP_1ST_PERIOD': METRICS_SKIP_1ST_PERIOD.lower() == 'true',
    'METRICS_STEP': int(METRICS_STEP)
})

logger.info(CONF)
