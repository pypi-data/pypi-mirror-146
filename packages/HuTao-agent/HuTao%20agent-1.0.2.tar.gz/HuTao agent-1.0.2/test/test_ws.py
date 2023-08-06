# -*- coding: utf-8 -*-

# @File    : test_ws.py
# @Date    : 2022-01-26
# @Author  : chenbo

__author__ = 'chenbo'

import time

from walnut_agent.script.operation import IosOpt
from walnut_agent.script.util_handle import setting


def start_wda():
    ios_opt = IosOpt(udid='679c48afa066538330baad04892da34b5264bf55')
    # ios_opt.install_wda(setting.app.ipa_path, bundle_id='com.bixin.runner.xctrunner')
    # print(ios_opt.start_wda().msg)
    # print(ios_opt.install_wda_built().msg)
    ios_opt.start_wda(bundle_id='com.bixin.runner.xctrunner')
    time.sleep(3)
    print(ios_opt.get_info())


if __name__ == '__main__':
    start_wda()
