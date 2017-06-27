# -*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event
import Index
import inspect
import os
from Service import LogginMange


class windowService(win32serviceutil.ServiceFramework):
    """
    Usage: 'PythonService.py [options] install|update|remove|start [...]|stop|restart [...]|debug [...]'
    Options for 'install' and 'update' commands only:
     --username domain\username : The Username the service is to run under
     --password password : The password for the username
     --startup [manual|auto|disabled|delayed] : How the service starts, default = manual
     --interactive : Allow the service to interact with the desktop.
     --perfmonini file: .ini file to use for registering performance monitor data
     --perfmondll file: .dll file to use when querying the service for
       performance data, default = perfmondata.dll
    Options for 'start' and 'stop' commands only:
     --wait seconds: Wait for the service to actually start or stop.
                     If you specify --wait with the 'stop' option, the service
                     and all dependent services will be stopped, each waiting
                     the specified period.
    """
    # 服务名
    _svc_name_ = "ServerService"
    # 服务显示名称
    _svc_display_name_ = "Server Service Monitor"
    # 服务描述
    _svc_description_ = "Server Monitor"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.server = Index.ServerMonitoring()
        self.logger = self.getlogger()
        self.isAlive = True

    def getlogger(self):
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        logger =LogginMange.LogginMange(dirpath+'/Log', "Service")
        return logger

    def SvcDoRun(self):
        import time
        self.logger.info("svc do run....")
        self.server.start()
        while self.isAlive:
            self.logger.info("I am alive.")
            time.sleep(1)
        #     # 等待服务被停止
        #     # win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        # 先告诉SCM停止这个过程
        self.logger.error("svc do stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(windowService)