#!usr/bin/env pyhton
#coding:utf-8

import sys
import os

import atexit
import time
import psutil

time.sleep(3)

line_num = 1


class ServerMonitor:
    def __init__(self):
        print "开始进行服务器监控"

    # 获取CPU状态;
    def getCPUstate(self,interval=1):
        return psutil.cpu_percent(interval)

    # 获取电脑内存使用状态
    def getMemorystate(self):
        phymem = psutil.virtual_memory()
        line = "Memory: %5s%% %6s/%s" % (
            phymem.percent,
            str(int(phymem.used / 1024 / 1024)) + "M",
            str(int(phymem.total / 1024 / 1024)) + "M"
        )
        return line

    def bytes2human(self,n):
        """
        >>> bytes2human(10000)
        '9.8 K'
        >>> bytes2human(100001221)
        '95.4 M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f %s' % (value, s)
        return '%.2f B' % (n)

    def poll(self,interval):
        """Retrieve raw stats within an interval window."""
        tot_before = psutil.net_io_counters()
        pnic_before = psutil.net_io_counters(pernic=True)
        # 休眠一段时间
        time.sleep(interval)
        tot_after = psutil.net_io_counters()
        pnic_after = psutil.net_io_counters(pernic=True)
        # 获取cpu状态
        cpu_state = self.getCPUstate(interval)
        # 获取内存使用状态
        memory_state = self.getMemorystate()
        return (tot_before, tot_after, pnic_before, pnic_after, cpu_state, memory_state)


    def refresh_window(self,tot_before, tot_after, pnic_before, pnic_after, cpu_state, memory_state):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")
        """Print stats on screen."""

        # print current time #cpu state #memory
        print(time.asctime() + " | " + cpu_state + " | " + memory_state)

        # totals
        print(" 网络状态:")
        print("total bytes:                     sent: %-10s     received: %s" % (self.bytes2human(tot_after.bytes_sent),
                                                                                 self.bytes2human(tot_after.bytes_recv))
              )
        print("total packets:                 sent: %-10s     received: %s" % (tot_after.packets_sent,
                                                                               tot_after.packets_recv)
              )
        # per-network interface details: let's sort network interfaces so
        # that the ones which generated more traffic are shown first
        print("")
        nic_names = pnic_after.keys()
        # nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
        for name in nic_names:
            stats_before = pnic_before[name]
            stats_after = pnic_after[name]
            templ = "%-15s %15s %15s"
            print(templ % (name, "TOTAL", "PER-SEC"))
            print(templ % (
                "发送的bytes",
                self.bytes2human(stats_after.bytes_sent),
                self.bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s',
            ))
            print(templ % (
                "接收的bytes",
                self.bytes2human(stats_after.bytes_recv),
                self.bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s',
            ))
            print(templ % (
                "发送的数据包",
                stats_after.packets_sent,
                stats_after.packets_sent - stats_before.packets_sent,
            ))
            print(templ % (
                "接收的数据包",
                stats_after.packets_recv,
                stats_after.packets_recv - stats_before.packets_recv,
            ))
            print("")

    # def Start(self):
    #     try:
    #         while True:
    #             interval = 5
    #             args = self.poll(interval)
    #             self.refresh_window(*args)
    #
    #     except Exception,e:
    #         print e.message




