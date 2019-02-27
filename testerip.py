#-*- coding:utf-8 -*-
import time
import aiohttp
import asyncio
from reidsclient import RedisClient

TEST_URL = 'https://cd.lianjia.com/ershoufang/'
VALID_STATUS_CODES = [200]
BATCH_TEST_SIZE = 50


class TesterIp(object):
    def __init__(self):
        """连接Redis"""
        self.db = RedisClient()

    async def test_single_proxy(self, proxy):
        """测试单个代理"""
        conn = aiohttp.TCPConnector(verify_ssl=False)  #连接池
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print("正在测试", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.db.max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.db.decrease(proxy)
                        print("请求响应码不合法", proxy)
            except (AttributeError,aiohttp.client_exceptions.ClientConnectionError,asyncio.TimeoutError,aiohttp.ClientError,aiohttp.client_exceptions.ClientResponseError):
                self.db.decrease(proxy)
                print("代理请求失败", proxy)

    def run(self):
        """测试主函数"""
        print("测试器开始运行")
        try:
            proxis = self.db.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxis), BATCH_TEST_SIZE):
                test_proxies = proxis[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print("测试器发生错误", e.args)

if __name__ =='__main__':
    test = TesterIp()
    test.run()