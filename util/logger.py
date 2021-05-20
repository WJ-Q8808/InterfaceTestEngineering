# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         logger
# -*- coding: UTF-8 -*-
import logging
import time
import os

class BaseLogger:
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s [%(module)s] %(message)s"

    def init_logger(self):
        logging.basicConfig(level=self.LOG_LEVEL, format=self.LOG_FORMAT)

class Logger(object):

    def __init__(self, logger):
        '''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''
        ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        log_path = os.path.join(ROOT_PATH, '../logs/') # 日志路径

        # 创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # 如果case组织结构式 /testsuit/featuremodel/xxx.py ， 那么得到的相对路径的父路径就是项目根目录
        log_name = log_path + rq + '.logs'
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


base_logger = BaseLogger()
