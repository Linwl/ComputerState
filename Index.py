#!usr/bin/env python
#coding:utf-8

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from Service import ServerMonitor
import ConfigParser
from Service import LogginMange


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")


class Application(tornado.web.Application):
    '''
    Application配置类
    '''
    def __init__(self):
        handlers = [
            (r"/", IndexHandler)
        ]
        settings = dict(
            template_path = TEMPLATE_PATH,
            static_path = STATIC_PATH,
            debug = True
        )
        tornado.web.Application.__init__(self, handlers, **settings)



class IndexHandler(tornado.web.RequestHandler):

     def init_log(self):
         return  LogginMange.LogginMange("Index", "Config/logger.conf")

     def get(self):
        server = ServerMonitor.ServerMonitor()
        cpustatus =server.getCPUstate(1)
        memorystate =server.getMemorystate()
        self.render("Index.html",Cpu_Status =int(cpustatus),Memory_state = int(memorystate))

     def post(self):
         request = self.get_argument("Cpustatus")
         server = ServerMonitor.ServerMonitor()
         if(str(request) =='GetCpu'):
             cpustatus = server.getCPUstate(1)
             self.write(str(cpustatus))
         elif(str(request) =='GetMemory'):
             memorystate = server.getMemorystate()
             self.write(str(memorystate))
         else:
             self.init_log().debug("错误的请求!")


class ServerMonitoring():
    """
    服务器监控
    """
    # def __init__(self):
    #     self.log = LogginMange.LogginMange("Index", "Config/logger.conf")

    def start(self):
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open('Config/Init.congfig'), "rb")
            port = int(config.get('Server_config', 'port_one'))
            tornado.options.parse_command_line()
            http_server = tornado.httpserver.HTTPServer(Application())
            http_server.listen(port)
            tornado.ioloop.IOLoop.instance().start()
            self.log.info("开始服务器监控")
        except Exception, e:
            self.log.error(e.message)
