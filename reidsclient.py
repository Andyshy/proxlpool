#-*- coding:utf-8 -*-
from random import choice
import redis

MAX_SCORE = 100  #最高分
MIN_SCORE = 0  #最低分
INITIAL_SCORE = 10  #初始分
REDIS_HOST = '127.0.0.1'  #地址
REDIS_PORT = 6379  #端口
REDIS_PASSWORD = None  #密码
REDIS_KEY = 'proxies'  #键名称

class RedisClient(object):
    """操作redis数据库"""
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """redis连接,初始化一个StrictRedis类，建立redis连接"""
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """向redis添加代理，并设置初试分数"""
        if not self.db.zscore(REDIS_KEY, proxy):  #返回键为REDIS_KEY中的成员proxy的分数，没有返回nil
            self.db.zadd(REDIS_KEY, score, proxy)  #如果返回nil，就向键为REDIS_KET的zset中添加proxy，并设置其分数为score

    def random(self):
        """获取随机代理（先尝试得到最高分的，如果没有，就按照分数排名从高到低进行获取100个）"""
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)  #返回键为REDIS_KEY中分数在MAX_SCORE和MAX_SCORE中的值
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)  #返回键为REDIS_KEY中分数排名前100的值
            if len(result):
                return choice(result)
            else:
                return ''

    def decrease(self, proxy):
        """用于测试代理，代理请求失败一次扣1分，分数小于最小值则删除"""
        score = self.db.zscore(REDIS_KEY, proxy)
        if score > MIN_SCORE:
            print("代理", proxy, "当前分数", score, "减1分")
            return self.db.zincrby(REDIS_KEY, proxy, -1)  #键为REDIS_KEY中元素proxy的分数减去1分
        else:
            print("代理", proxy, "当前分数", score, "删除")
            return self.db.zrem(REDIS_KEY, proxy)  #键为REDIS_KEY的zset删除元素proxy

    def exists(self, proxy):
        """判断键为REDIAS_KEY的zset中是否存在proxy"""
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """如果测试代理可用，便设置其分数为100"""
        print("代理", proxy, "可用，设置为", MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """获取代理数量"""
        return self.db.zcard(REDIS_KEY)  #返回键为REDIS_KEY的zset中元素数量

    def all(self):
        """获取所有代理"""
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)



