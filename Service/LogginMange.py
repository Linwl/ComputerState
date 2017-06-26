#!/usr/bin/env python
# coding=utf-8

import logging.config
import logging
from time import strftime
from logging.handlers import RotatingFileHandler

class LogginMange(object):
    """
    Logging模块管理
    """
    _Version='1.0.2017.03.03'
    #通过配置文件路径设置日志参数
    def __init__(self,logname,confpath):
        logging.config.fileConfig(confpath)
        Rthandler = RotatingFileHandler('Log/'+logname+'_'+strftime("%Y-%m-%d")+'.log', maxBytes=10 * 1024 * 1024, backupCount=5)
        Rthandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        Rthandler.setFormatter(formatter)
        logging.getLogger('pyLog').addHandler(Rthandler)
        self.logger = logging.getLogger('pyLog')

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)