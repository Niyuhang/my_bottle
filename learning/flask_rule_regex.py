#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:flask_rule_regex.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2020 by the Niyuhang.
    :license: BSD, see LICENSE for more details.
"""
import re
from werkzeug.routing import Rule, Map

"""
?P<xx> 用来为后面匹配到的取名
"""
_rule_re = re.compile(
    r"""
    (?P<static>[^<]*)                           # static rule data
    <
    (?:
        (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
        (?:\((?P<args>.*?)\))?                  # converter arguments
        \:                                      # variable delimiter
    )?
    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)        # variable name
    >
    """,
    re.VERBOSE,
)

map_a = Map()
rule_a = Rule("/ds/<ds>/", endpoint="ds")
rule_a.bind(map_a)
print(rule_a._regex)
print(rule_a.match(u"/ds/d"))
# print(re.compile(r"\\s").match("\s"))


# print(_rule_re.match("/dsd/<sd>").end())

# regex_for_name = re.compile(r"(?P<number>\d+)")
# res = regex_for_name.match("123")
# print(res.groupdict()["number"])