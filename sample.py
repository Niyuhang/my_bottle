#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:sample.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2020 by the Niyuhang.
    :license: BSD, see LICENSE for more details.
"""
from my_bottle import MyBottle

app = MyBottle()


@app.route("/test")
def test():
    return "你好呀"

from flask import  Flask
app.run_server_forever()
