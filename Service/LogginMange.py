#!/usr/bin/env python
# coding=utf-8

import logging.config
import logging
from time import strftime
from logging.handlers import RotatingFileHandler
import inspect
import os
class LogginMange:
    """
    Logging模块管理
    """
    _Version='1.0.2017.03.03'
    #通过配置文件路径设置日志参数
    def __init__(self,logpath,logname):
        self.logger = self.get_logger(logpath,logname)

    def get_logger(self,logpath,logname):
        logger = logging.getLogger('['+logname+']')
        handler = logging.FileHandler(os.path.join(logpath, logname+'_'+strftime("%Y-%m-%d")+'.log'))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)