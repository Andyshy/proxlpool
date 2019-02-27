#-*- coding:utf-8 -*-
import time
from multiprocessing import Process
from getter import Getter
from testerip import TesterIp
from api_ip import app

TSETER_ENABLEED = True
GETTER_ENABLED = True
API_ENABLED = True


class SchedulerIp(object):
    """调度器 """
    def schedule_tester(self):
        """调用测试模块的控制开关，并让其进入死循环"""
        testerip = TesterIp()
        while True:
            print("测试器开始运行")
            testerip.run()
            time.sleep(10*60)

    def schedule_getter(self):
        """调用爬取模块的控制开关，让其进入死循环"""
        getter = Getter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(30*60)

    def schedule_api(self):
        print("API启动")
        app.run()

    def run(self):
        """生成两个进程，彼此独立运行"""
        print("代理池开始运行")
        if TSETER_ENABLEED:
            tester_process = Process(target=self.schedule_tester)  #Process生产测试模块的进程
            tester_process.start()  #开始进程
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)  #Process生产爬取模块的进程
            getter_process.start()  #开始进程
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ =='__main__':
    s = SchedulerIp()
    s.run()
