#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:socket_server.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2020 by the Niyuhang.
    :license: BSD, see LICENSE for more details.
"""

import os
import logging

import re
from socket import *
from multiprocessing import Process



def main():
    # 开启socket链接 作为服务端
    # 使用默认参数:
    # 地址簇 ipv4, family=AF_INET,
    #              type=SOCK_STREAM
    server_socket = socket()
    # 设置socket 在四次挥手后立即关闭 并且立即释放资源
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定监听地址 （host, port）
    logging.info("服务启动了")
    server_socket.bind(("0.0.0.0", 8080))

    server_socket.listen(128)  # 最多可以监听128个连接

    while True:
        # 监听请求

        # 收到请求后会得到对应socket请求对方和请求的地址
        # 并且利用这个socket和客户端进行信息传输
        socket_client, client_addr = server_socket.accept()

        # 这个时候子进程会把主进程里面的变量复制一遍 只在一方修改的时候进行分离
        # 由于子进程复制了这个socket_client 所以需要在主进程关闭socket
        this_process = Process(target=handle_request, args=(socket_client,))
        this_process.start()

        socket_client.close()


def handle_request(socket_client):
    """
    处理socket链接
    :param socket_client:
    :return:
    """
    logging.info("处理客户端请求了")
    recv_data = socket_client.recv(1024).decode("utf-8")  # 1024表示本次接收的最大字节数
    request_header_lines = recv_data.splitlines()
    # for line in request_header_lines:
    #     print(line)
    if not request_header_lines:
        file_name = "index.html"
    else:
        file_name = get_the_file_name(request_header_lines[0]) or "index.html"

    try:
        # 返回浏览器数据
        # 设置返回的头信息 header
        response_headers = "HTTP/1.2.1.2 200 OK\r\n"  # 200 表示找到这个资源
        response_headers += "\r\n"  # 空一行与body隔开
        # 设置内容body
        response_body = find_static_file_data(file_name)
    except:
        response_headers = "HTTP/1.2.1.2 404 NOT FOUND\r\n"  # 404
        response_headers += "\r\n"  # 空一行与body隔开
        response_body = ""

    # 合并返回的response数据
    response = response_headers + response_body
    socket_client.send(response.encode())
    socket_client.close()


def get_the_file_name(path):
    """
    匹配到/路由后到空格前的路径
    :param path: "GET / HTTP1.0"
    :return:
    """
    pattern = re.compile(r"(?:[^/]+)/([^?\s]*)")
    res = pattern.match(path)
    if res:
        return res.groups()[0]


def find_static_file_data(file_name: str):
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "htmls", file_name)
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        raise ValueError(e)


if __name__ == '__main__':
    main()
