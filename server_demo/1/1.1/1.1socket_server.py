#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:1.2.1socket_server.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2020 by the Niyuhang.
    :license: BSD, see LICENSE for more details.
"""
import logging
from socket import *


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
        handle_request(socket_client)


def handle_request(socket_client):
    """
    处理socket链接
    :param socket_client:
    :return:
    """
    logging.info("处理客户端请求了")
    recv_data = socket_client.recv(1024).decode("utf-8")  # 1024表示本次接收的最大字节数

    #print("client_recv:",recv_data)
    request_header_lines = recv_data.splitlines()
    for line in request_header_lines:
        print("line", line)

    # 返回浏览器数据
    # 设置返回的头信息 header
    response_headers = "HTTP/1.2.1.2 200 OK\r\n" # 200 表示找到这个资源
    response_headers += "\r\n" # 空一行与body隔开
    # 设置内容body
    response_body = '''
                        <!DOCTYPE html>
                    <html lang="en",>
                    <head>
                        <meta charset="UTF-8">
                        <title>Title</title>
                    </head>
                    <body>  
                        <h1> 你好呀 小天才</h1>
                    </body>
                    </html>
    '''

    # 合并返回的response数据
    response = response_headers + response_body
    socket_client.send(response.encode())
    socket_client.close()


if __name__ == '__main__':
    main()