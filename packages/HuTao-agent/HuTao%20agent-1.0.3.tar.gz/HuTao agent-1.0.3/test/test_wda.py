# -*- coding: utf-8 -*-

# @File    : test_wda.py
# @Date    : 2022-01-22
# @Author  : chenbo

__author__ = 'chenbo'

import wda


def init():
    c = wda.Client('http://127.0.0.1:8200')
    print(c.source())
    # c.click(339, 273)
    # c.home()


if __name__ == '__main__':
    init()
