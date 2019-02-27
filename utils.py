#-*- coding:utf-8 -*-
import datetime
import requests
from fake_useragent import UserAgent

ua = UserAgent()

def get_page(url):
    headers = {'User-Agent':ua.random}
    try:
        print("开始爬取", datetime.datetime.now(), url)
        response = requests.get(url, headers = headers)
        if response.status_code == 200 and len(response.text) > 300:
            print("爬取成功", datetime.datetime.now(), url)
            return response.text
    except Exception as e:
        print("爬取失败", e)