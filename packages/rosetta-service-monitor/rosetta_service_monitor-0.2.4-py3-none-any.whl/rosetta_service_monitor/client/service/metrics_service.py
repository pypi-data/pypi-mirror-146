#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: mq_service.py 
@time: 2021/08/09
@contact: 
@site:  
@software: PyCharm 
"""
import asyncio
import json
import socket
import threading
from traceback import format_exc

import aiohttp
from kafka import KafkaProducer
import os

from loguru import logger

from rosetta_service_monitor.client.metrics_conf import CONF
from rosetta_service_monitor.client.enums import WarnningType
from rosetta_service_monitor.client.service import MQBaseService, MQNoUseService


class MetricsService(MQBaseService):
    def __init__(self, conf):
        super(MetricsService, self).__init__()
        self.METRICS_AGENT_HOST = conf.METRICS_AGENT_HOST
        self.url = f'{self.METRICS_AGENT_HOST}/metrics_api'
        self.METRICS_APP_NAME = conf.METRICS_APP_NAME
        self.METRICS_APP_VERSION = conf.METRICS_APP_VERSION
        self.METRICS_SERVICE_NAME = conf.METRICS_SERVICE_NAME
        self.METRICS_SKIP_1ST_PERIOD = conf.METRICS_SKIP_1ST_PERIOD
        self.METRICS_STEP = conf.METRICS_STEP

    async def post_data(self, data=None):
        # logger.debug(f'url: {self.url}, data: {data}')
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=data) as resp:
                return await resp.text()

    async def send_mq(self, project_name: str, err_msg: str, trace_id: str, request: dict,
                      warnning_type: WarnningType = WarnningType.normal, **kwargs):
        pass

    async def send_metrics(self, defmodel):
        data = {
            "app_name": self.METRICS_APP_NAME,
            "app_ver": self.METRICS_APP_VERSION,
            "service_name": self.METRICS_SERVICE_NAME,
            "step": self.METRICS_STEP,
            "ver": "0.1",
            "skip_1st_period": self.METRICS_SKIP_1ST_PERIOD,
            "defmodel": defmodel
        }

        await self.post_data(data=data)

    def send_async(self, defmodel):
        r = self.async_run(self.send_metrics, defmodel)
        return r

    def close(self):
        pass


metrics_service = MetricsService(conf=CONF)
