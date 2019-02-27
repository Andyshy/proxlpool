#-*- coding:utf-8 -*-
import json
from pyquery import PyQuery as pq
from utils import get_page


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):  #eval()将字符串当成有效的表达式使用
            print("成功获取代理",proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=3):
        start_url = 'http://www.66ip.cn/areaindex_35/{0}.html'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()  #gt(0)第一个节点之后的节点
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()  #nth-child(1)第一个节点
                    port = tr.find('td:nth-child(2)').text()  #nth-child(2)第二个节点
                    yield ':'.join([ip, port])
    def crawl_360(self, page_count=10):
        start_url = 'http://www.swei360.com/free/?page={0}'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#container table tbody tr').items()  #gt(0)第一个节点之后的节点
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()  #nth-child(1)第一个节点
                    port = tr.find('td:nth-child(2)').text()  #nth-child(2)第二个节点
                    yield ':'.join([ip, port])

    def crawl_xici(self, page_count=3):
        start_url = 'http://www.xicidaili.com/nn/{0}'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#wrapper .clearfix #ip_list tr:gt(0)').items()  #gt(0)第一个节点之后的节点
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()  #nth-child(1)第一个节点
                    port = tr.find('td:nth-child(3)').text()  #nth-child(2)第二个节点
                    yield ':'.join([ip, port])

    def crawl_kuaidaili(self,page_count=3):
        start_url = 'https://www.kuaidaili.com/free/inha/{0}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#list table tbody tr').items()  # gt(0)第一个节点之后的节点
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()  # nth-child(1)第一个节点
                    port = tr.find('td:nth-child(2)').text()  # nth-child(2)第二个节点
                    yield ':'.join([ip, port])






