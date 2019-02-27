#-*- coding:utf-8 -*-
from flask import Flask,g
from reidsclient import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random()
