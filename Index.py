#!usr/bin/env python
#coding:utf-8

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from Service import ServerMonitor

define("port", default=6411, help="run on the given port", type=int)

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
    def get(self):
        server =ServerMonitor.ServerMonitor()
        cpustatus =server.getCPUstate(1)
        memorystate =server.getMemorystate()
        self.render("Index.html",Cpu_Status =int(cpustatus),Memory_state = memorystate)




def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
