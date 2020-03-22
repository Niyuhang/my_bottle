#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:my_bottle.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2020 by the Niyuhang.
    :license: BSD, see LICENSE for more details.

"""
from gevent.pywsgi import WSGIServer


class SingleTon:

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, "_instance"):
            return cls._instance
        else:
            instance = super(SingleTon, cls).__new__(cls, *args, **kwargs)
            cls._instance = instance
            return instance


class MyBottle(SingleTon):

    def __init__(self):
        self.routes = []

    def wsgi_app(self, environ, start_response):
        # 分发到对应的路由 并且得到结果
        headers = [('Content-Type', 'text/html; charset=UTF-8')]
        try:
            res = self.dispatch_request(environ)
            start_response("200 OK", headers=headers)
        except Exception:
            res = "失败了"
            start_response("500 INTERNAL SERVER ERROR", headers=headers)
        return [res.encode()]

    def dispatch_request(self, environ):
        """
        分发请求到对应函数并且执行
        """
        current_path = environ.get("PATH_INFO")
        for path in self.routes:
            match_res, values = self.match(path["path"], current_path)
            if match_res:
                res = path["func"](*values)
                return res
        else:
            return "没找到"

    @staticmethod
    def match(path: str, current_path: str) -> (bool, list):
        """
        比对两个路由是否匹配 /a/<mateiral_id>  /a/1
        :param path:
        :param current_path:
        :return: (bool, list)
        """
        return True, []

    def route(self, path: str):
        """
        注册路由
        """

        def decorate(f):
            self.add_url_for_app(path, f)

            def wrap(*args, **kwargs):
                return f(*args, **kwargs)

            return wrap

        return decorate

    def add_url_for_app(self, path: str, f):
        """
        给app增加路由
        :param path:
        :param f:
        :return:
        """
        self.routes.append({"path": path, "func": f})

    def run_server_forever(self, host="", port=None):
        port = port or 8080
        server = WSGIServer((host, port), self)
        server.serve_forever()

    run = run_server_forever

    def __call__(self, environ, start_response):
        """
        每次在接收到请求的时候就会调用
        :param environ:
        :param start_response:
        :return:
        """
        return self.wsgi_app(environ, start_response)
