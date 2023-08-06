#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: baskground_task_actor.py 
@time:
@contact: 
@site:  
@software: PyCharm 
"""
import asyncio
import os
import threading
from asyncio import events
from asyncio.runners import _cancel_all_tasks
from queue import Queue
from threading import Event, Thread
from traceback import format_exc

from loguru import logger


class ActorExit(Exception):
    pass


class Actor:
    # _instance_lock = threading.Lock()

    def __init__(self):
        self._mailbox = Queue(maxsize=int(os.environ.get("QUEUE_MAX_SIZE", 0)))
        self.start()

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(Actor, "_instance"):
    #         with Actor._instance_lock:
    #             if not hasattr(Actor, "_instance"):
    #                 Actor._instance = super(Actor, cls).__new__(cls, *args, **kwargs)
    #     return Actor._instance

    def send(self, msg):
        """
        发送任务到队列
        """
        self._mailbox.put(msg)

    def recv(self):
        """
        从队列获取任务，如果任务为终止信号，开始退出
        """
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        """
        发送终止信号，线程友好退出
        """
        self.send(ActorExit)

    def start(self):
        """
        启动后台线程
        """
        self._terminated = Event()
        t = Thread(target=self._bootstrap)

        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            # event 释放
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        """
        Run method to be implemented by the user
        """
        while True:
            msg = self.recv()


# 后台任务设置结果
class Result:
    def __init__(self):
        # 通过event来控制结果的获取
        self._evt = Event()
        self._result = None

    def set_result(self, value):
        self._result = value
        self._evt.set()

    def result(self):
        self._evt.wait()
        return self._result


class BackgroundWorker(Actor):
    def submit(self, func, *args, **kwargs):
        """
        用于提交任务
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        r = Result()
        self.send((func, args, kwargs, r))
        return r

    def run(self):
        """
        后台线程，用于从队列中获取代执行的后台任务执行
        :return:
        """
        loop = events.new_event_loop()
        try:
            events.set_event_loop(loop)
            while True:
                func, args, kwargs, r = self.recv()
                resp = None
                if asyncio.iscoroutinefunction(func):
                    try:
                        loop.run_until_complete(func(*args, **kwargs))
                    except Exception as err:
                        info = f'{err.__class__.__name__}:{err}\n{format_exc()}\n'
                        logger.warning(info)
                else:
                    try:
                        resp = func(*args, **kwargs)
                    except Exception as err:
                        info = f'{err.__class__.__name__}:{err}\n{format_exc()}\n'
                        logger.warning(info)
                r.set_result(resp)
        finally:
            try:
                _cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                events.set_event_loop(None)
                loop.close()
