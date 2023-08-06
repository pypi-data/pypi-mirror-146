# -*- coding: utf-8 -*-

# @File    : operation.py
# @Date    : 2022-04-07
# @Author  : chenbo

__author__ = 'chenbo'

from pathlib import Path
from typing import Union, List

from loguru import logger
from tidevice import Device, exceptions

from walnut_agent.common import config
from walnut_agent.script.app_handle import tid, _xctestThread, CmdThread
from walnut_agent.script.case_class import Feature
from walnut_agent.script.util_handle import setting


class IosOpt:
    udid: str = ''
    bundle_id: str = ''
    device: Device = None
    prot: int = None

    def __init__(self, udid: str):
        self.udid = udid
        self.device = Device(self.udid)

    def install(self, path: Union[str, Path]) -> Feature:
        """安装成功后返回"""
        try:
            logger.debug(f'开始安装[{path}]')
            bundle_id = self.device.app_install(str(path))
            logger.debug(f"安装包[{path}]成功:{bundle_id}")
            return Feature.success().set_data(bundle_id)
        except exceptions.ServiceError:
            logger.error("应用认证异常，安装失败！")
            return Feature.fail().set_data('应用认证异常，安装失败！')

    def app_list(self) -> List[str]:
        """
        查询第三方列表
        """
        instruments = self.device.connect_instruments()
        # 设备上全部App信息列表 包含 系统应用和插件，通过 Type 可以区分App
        apps = instruments.app_list()
        # 只筛选用户安装的App列表
        user_app_list = [app for app in apps if app["Type"] == "User"]
        return user_app_list

    def uninstall(self, pkg_name: str):
        self.device.app_uninstall(pkg_name)

    def install_wda(self, path: Union[str, Path], bundle_id: str = None) -> Feature:
        """com.facebook.WebDriverAgentRunner.xctrunner"""
        "CFBundleIdentifier"
        for app_info in self.app_list():
            if app_info["CFBundleIdentifier"] == bundle_id:
                logger.debug(f"已安装: {self.bundle_id}")
                self.bundle_id = bundle_id
        f: Feature = self.install(path)
        if f.is_success():
            self.bundle_id = f.data
        return f

    def install_wda_built(self, path: Union[str, Path] = None, bundle_id: str = None) -> Feature:
        packages = []
        if path:
            packages.append(path)
        packages.append(setting.app.runner_path)
        packages.append(setting.app.ipa_path)

        for package_path in packages:
            f = self.install_wda(package_path, bundle_id)
            if f.is_success():
                return f
        return Feature.fail().set_message(f"安装iOS驱动包失败:{path}")

    def start_wda(self, bundle_id: str = None, port: int = 8200) -> Feature:
        """
        必须udid启动 WebDriverAgent
        port = 8200  这里后期如果需要运行多台设备，请使用动态端口
        tidevice -u 679c48afa066538330baad04892da34b5264bf55 wdaproxy -B com.facebook.WebDriverAgentRunner.ht2022.xctrunner --port 8100
        tidevice -u 00008030-000C05612110802E wdaproxy -B com.facebook.WebDriverAgentLib1638862464.xctrunner --port 8100
        wdaproxy -p 8100 -u 679c48afa066538330baad04892da34b5264bf55
        通过访问  http://127.0.0.1:8200/status  确定 WebDriverAgent 的链接状态
        """
        if self.udid not in tid.get_devices():
            return "设备未连接！"
        if bundle_id: self.bundle_id = bundle_id
        _xctest_t = _xctestThread(udid=self.udid, port=port, bundle_id=self.bundle_id)
        _iproxy_t = CmdThread(f"tidevice -u {self.udid} relay {port} 8100", 3000)
        _xctest_t.start()
        _iproxy_t.start()
        self.prot = port
        return Feature.success().set_message(f"WebDriverAgent start successful: http://127.0.0.1:{port}")

    def get_info(self) -> dict:
        """
        获取设备信息,为appium 启动做初始化准备
        """
        info = Device(self.udid).device_info()
        try:
            model = config.iphone_model[info["ProductType"]]
        except KeyError as e:
            model = None
            logger.warning("设备[{0}]marketName[{1}]无法解析!".format(self.udid, info["ProductType"]))
        return {
            "platformName": "iOS",
            "appium:platformVersion": info["ProductVersion"],
            "appium:udid": self.udid,
            "appium:deviceName": model,
            "appium:bundleId": self.bundle_id,
            "appium:noReset": True,
            "relaxedSecurityEnabled": True,
            "appium:automationName": "XCUITest",
            "unicodeKeyboard": True,
            "resetKeyboard": True
        }