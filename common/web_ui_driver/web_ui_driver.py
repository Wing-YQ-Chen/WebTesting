import logging
import os
import pkgutil
import re
import subprocess
import time
from typing import Union, Optional, List, Literal
from func_timeout import func_set_timeout
from selenium.common import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.remote.command import Command
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.driver_finder import DriverFinder
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.relative_locator import RelativeBy
from selenium.webdriver import ChromeOptions
from .web_ui_element import WebUiElement
from .web_ui_element import ElmWith

class WebUiDriver(RemoteWebDriver):
    """
    针对WebDriver的封装，拓展常用功能和日志，最重要是改造了find_element
    目前有个缺陷是只支持SG模式
    """

    _web_element_cls = WebUiElement
    BIZ_NAME: str

    def __init__(self,
                 command_executor: str = "http://127.0.0.1:4444",
                 options: Optional[Union[BaseOptions, List[BaseOptions]]] = None,
                 loger: logging.Logger = logging.getLogger(),
                 ) -> None:
        """
        初始化 WebUiDriver 实例。

        :param command_executor: 命令执行器的地址，默认为 "http://127.0.0.1:4444"，可以是字符串或 RemoteConnection 对象。
        :param keep_alive: 是否保持连接，默认为 True。
        :param file_detector: 文件检测器，可选。
        :param options: 浏览器选项，可以是单个 BaseOptions 对象或 BaseOptions 对象列表，默认为 None。
        :param loger: 日志记录器，默认为获取的默认日志记录器。
        """
        self.loger = loger

        if options is None:
            options = ChromeOptions()
            options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 避免终端下执行代码报警告
            options.add_argument("--ignore-certificate-errors")  # 忽略提醒，证书错误
            options.add_argument("--ignore-ssl-errors")
            options.add_argument("–disable-notifications")
            options.add_argument("lang=en_US")
            options.add_experimental_option("detach", True)  # 引入不关闭浏览器的相关配置项
            # options.add_extension('插件')  # 加载拓展插件
            # options.add_argument('--headless')  # 开启无界面模式,如果涉及到与网页的交互（输入内容，点击按钮）那么有些网站就不能使用无头浏览器
            # options.add_argument("--disable-gpu")  # 禁用gpu
            # options.add_argument('--user-agent=Mozilla/5.0 HAHA')  # 配置对象添加替换User-Agent的命令
            # options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
            # options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
            # options.add_argument('--incognito')  # 隐身模式（无痕模式）
            # options.add_argument('--disable-javascript')  # 禁用javascript
            # options.add_argument(f"--proxy-server=http://115.239.102.149:4214")  # 使用代理
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            # user_dir = r'./browser_cache'
            # options.add_argument(f"--user-data-dir={user_dir}") # 加载用户缓存，可以记录使用记录和cookie，如果不指定缓存路径，会自动创建临时文件夹。
            # options.add_experimental_option('mobileEmulation', {'deviceName': 'Galaxy S5'}) # 模拟手机浏览器

        self.loger.info('✈️ Lunching Browser')
        if command_executor == 'LOCAL':
            service = ChromiumService(log_output=subprocess.STDOUT)
            finder = DriverFinder(service, options)
            if finder.get_browser_path():
                options.binary_location = finder.get_browser_path()
                options.browser_version = None

            service.path = service.env_path() or finder.get_driver_path()
            service.start()

            command_executor = ChromiumRemoteConnection(remote_server_addr=service.service_url,
                                                        browser_name='chrome',
                                                        vendor_prefix='goog')

        super().__init__(command_executor, options=options)
        self.init_timeout = 10
        self.implicitly_wait(self.init_timeout)
        self.maximize_window()

    def __call__(self,
                 biz_name='',
                 timeout: int = 10,
                 ignore_err: bool = False,
                 errmsg: str = '',
                 **kwargs) -> WebUiElement:
        """
        根据给定的参数查找并返回一个 WebUiElement。

        :param biz_name: 业务名称，默认为空字符串。
        :param timeout: 查找元素的超时时间，默认为10秒。
        :param raise_err: 是否在找不到元素时抛出异常，默认为 True。
        :param errmsg: 错误消息，默认为空字符串。
        :param kwargs: 包含定位元素的参数，如 id、xpath 等。
        :return: 找到的 WebUiElement。
        """
        check_by_list = [ElmWith.ID,
                         ElmWith.XPATH,
                         ElmWith.LINK_TEXT,
                         ElmWith.PARTIAL_LINK_TEXT,
                         ElmWith.NAME,
                         ElmWith.TAG_NAME,
                         ElmWith.CLASS_NAME,
                         ElmWith.CSS_SELECTOR]
        by = ''
        value = ''
        for i in check_by_list:
            if kwargs.get(i):
                if by:
                    raise KeyError('Please specify only one locator')
                by = i
                value = kwargs.get(i)

        return self.find_element(by,
                                 value,
                                 biz_name,
                                 timeout,
                                 ignore_err,
                                 errmsg)

    def get(self, url: str) -> None:
        """
        导航到指定的 URL。

        :param url: 要访问的 URL 字符串。
        """
        self.loger.info(f"🌍 Accessing URL: {url}")
        super().get(url)

    def create_web_element(self, element_id: str) -> WebUiElement:
        """
        创建一个 WebUiElement。

        :param element_id: 元素的 ID。
        :return: 创建的 WebUiElement。
        """
        return WebUiElement(self, element_id, self.loger, self.BIZ_NAME)

    def wait_elm(self,
                 appearance: bool = False,
                 biz_name='',
                 timeout: int = 60,
                 errmsg: str = '',
                 **kwargs) -> bool:
        """
        等待元素出现或消失。

        :param appearance: 是否等待元素出现，默认为 False，表示等待元素消失。
        :param biz_name: 业务名称，默认为空字符串。
        :param timeout: 等待的超时时间，默认为60秒。
        :param errmsg: 错误消息，默认为空字符串。
        :param kwargs: 包含定位元素的参数。
        :return: 如果元素按预期出现或消失，则返回 True，否则返回 False。
        """
        if appearance:
            if self(biz_name, timeout, False, **kwargs):
                return True
            else:
                if errmsg:
                    logging.error(errmsg)
                    raise TimeoutError(errmsg)
                else:
                    errmsg = errmsg if errmsg else f'long time not appear {self.BIZ_NAME}'
                    logging.error(errmsg)
                return False

        else:
            # time.sleep(1)
            for s in range(timeout * 2):
                if self(biz_name, 0, False, **kwargs):
                    time.sleep(0.5)
                    continue
                else:
                    return True
            else:
                if errmsg:
                    logging.error(errmsg)
                    raise TimeoutError(errmsg)
                else:
                    errmsg = errmsg if errmsg else f'long time not disappear {self.BIZ_NAME}'
                    logging.error(errmsg)
                    return False

    def find_element(self,
                     by: Literal[
                             "id",
                             "xpath",
                             "link text",
                             "partial link text",
                             "name",
                             "tag name",
                             "class name",
                             "css selector"
                         ] | None = By.ID,
                     value: Optional[str] = None,
                     biz_name='',
                     timeout: int = 10,
                     ignore_err: bool = False,
                     errmsg: str = ''
                     ) -> WebUiElement:
        """
        查找单个元素。

        :param by: 定位方式，如 "id"、"xpath"等，默认为 By.ID。
        :param value: 定位的值，根据 by 的类型而定，默认为 None。
        :param biz_name: 业务名称，默认为空字符串。
        :param timeout: 查找元素的超时时间，默认为10秒。
        :param ignore_err: 是否在找不到元素时抛出异常，默认为 True。
        :param errmsg: 错误消息，默认为空字符串。
        :return: 找到的 WebUiElement。
        """
        if biz_name:
            self.BIZ_NAME = "[{}]".format(biz_name)
        else:
            self.BIZ_NAME = '[{}]:[{}]'.format(by, value)
        self.loger.info('🔍 Finding element for {}'.format(self.BIZ_NAME))

        self.implicitly_wait(timeout)
        try:
            if isinstance(by, RelativeBy):
                elements: [WebUiElement] = self.find_elements(by=by, value=value, BIZ_NAME=self.BIZ_NAME)
                if not elements:
                    raise NoSuchElementException()
                elements[0].highlight()
                self.implicitly_wait(self.init_timeout)
                return elements[0]

            if by == By.ID:
                by = By.CSS_SELECTOR
                value = f'[id="{value}"]'
            elif by == By.CLASS_NAME:
                by = By.CSS_SELECTOR
                value = f".{value}"
            elif by == By.NAME:
                by = By.CSS_SELECTOR
                value = f'[name="{value}"]'
            element: WebUiElement = self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
            element.highlight()
            self.implicitly_wait(self.init_timeout)
            return element
        except BaseException:
            self.implicitly_wait(self.init_timeout)
            msg = '⛔ Not Found Element {} by [{}]:[{}]'.format(biz_name, by, value)
            self.loger.error(msg)
            if not ignore_err:
                if errmsg:
                    raise NoSuchElementException(errmsg)
                else:
                    raise NoSuchElementException(msg)

    def find_elements(self,
                      by: Literal[
                              "id",
                              "xpath",
                              "link text",
                              "partial link text",
                              "name",
                              "tag name",
                              "class name",
                              "css selector"
                          ] or None = By.ID, value: Optional[str] = None, BIZ_NAME=''
                      ) -> List[WebUiElement]:
        """
        查找多个元素。

        :param by: 定位方式，如 "id"、"xpath"等，默认为 By.ID。
        :param value: 定位的值，根据 by 的类型而定，默认为 None。
        :param BIZ_NAME: 业务名称，默认为空字符串。
        :return: 找到的 WebUiElement 列表。
        """
        # self.BIZ_NAME = BIZ_NAME
        if isinstance(by, RelativeBy):
            _pkg = ".".join(__name__.split(".")[:-1])
            raw_function = pkgutil.get_data(_pkg, "findElements.js").decode("utf8")
            find_element_js = f"/* findElements */return ({raw_function}).apply(null, arguments);"
            return self.execute_script(find_element_js, by.to_dict())

        if by == By.ID:
            by = By.CSS_SELECTOR
            value = f'[id="{value}"]'
        elif by == By.CLASS_NAME:
            by = By.CSS_SELECTOR
            value = f".{value}"
        elif by == By.NAME:
            by = By.CSS_SELECTOR
            value = f'[name="{value}"]'

        # Return empty list if driver returns null
        # See https://github.com/SeleniumHQ/selenium/issues/4555
        return self.execute(Command.FIND_ELEMENTS, {"using": by, "value": value})["value"] or []

    def quit(self) -> None:
        """
        关闭浏览器。
        """
        self.loger.info('🛬 Quiting browser')
        try:
            self.__quit_browser()
        except BaseException:
            self.loger.info('Quit browser failed')

    @func_set_timeout(5)
    def __quit_browser(self):
        """
        尝试在5秒内关闭浏览器，内部调用父类的 quit 方法。
        """
        super().quit()

    def close_pages(self, except_re_list: [str] = list):
        """
        关闭除了标题匹配 except_re_list 中字符串的页面之外的所有页面。

        :param except_re_list: 要保留的页面标题的正则表达式列表，默认为空列表。
        """
        temp = self.window_handles
        for handle in temp:
            try:
                self.switch_to.window(handle)
            except BaseException:
                self.loger.info(f"This window not existing already '{handle}'")
                continue
            title = self.title
            self.loger.info(f"title is '{title}'")
            for re_str in except_re_list:
                if re.findall(re_str, title):
                    break
            else:
                self.loger.info(f"Closing window '{title}'")
                self.close()

    def switch_frame(self, frame_reference=None):
        """
        切换到指定的 frame，如果 frame_reference 为 None，则切换到默认内容。

        :param frame_reference: 要切换到的 frame 的引用，可以是 frame 的名称、ID 或 frame 元素本身。
        """
        if frame_reference:
            self.switch_to.frame(frame_reference)
        else:
            self.switch_to.default_content()

    def screenshot(self, save_dir_path=".", file_name: str = "", full_flag: bool = False,
                   height_multiplier: float = 1, width_multiplier: float = 1):
        """
        截取屏幕截图。

        :param save_dir_path: 保存截图的目录路径，默认为当前目录。
        :param file_name: 截图文件名，默认为当前时间命名的文件名。
        :param full_flag: 是否截取整个页面，默认为 False。
        :param height_multiplier: 高度缩放倍数，默认为1。
        :param width_multiplier: 宽度缩放倍数，默认为1。
        :return: 截图保存的路径，如果失败则返回相应的错误信息。
        """
        if not save_dir_path:
            return ""
        if not file_name:
            file_name = '{} Web.png'.format(time.strftime('%Y%m%d%H%M%S', time.localtime()).__str__())
        try:
            return self.__screenshot(save_dir_path, file_name, full_flag, height_multiplier, width_multiplier)
        except BaseException:
            return "Fail to take screenshot"

    @func_set_timeout(5)
    def __screenshot(self, save_dir_path, file_name, full_flag, height_multiplier, width_multiplier):
        """
        内部方法，用于实际执行截图操作，设置窗口大小、保存截图并恢复窗口大小。

        :param save_dir_path: 保存截图的目录路径。
        :param file_name: 截图文件名。
        :param full_flag: 是否截取整个页面。
        :param height_multiplier: 高度缩放倍数。
        :param width_multiplier: 宽度缩放倍数。
        :return: 截图保存的路径。
        """
        current_width = self.get_window_size()['width']
        current_height = self.get_window_size()['height']
        if full_flag:
            body_width = self.execute_script("return document.body.scrollWidth")
            body_height = self.execute_script("return document.body.scrollHeight")
            self.set_window_size(body_width * width_multiplier, body_height * height_multiplier)
            time.sleep(0.5)
        save_dir_path = os.path.abspath(save_dir_path)
        if not os.path.exists(save_dir_path):
            os.makedirs(save_dir_path)
        save_path = os.path.join(save_dir_path, file_name)
        self.save_screenshot(save_path)
        if full_flag:
            self.set_window_size(current_width, current_height)
        return save_path

    def alert(self, time_out=5, raise_err_not_alert=False) -> 'Alert':
        for i in range(time_out * 2):
            try:
                return self.switch_to.alert
            except Exception:
                time.sleep(0.5)
        msg = 'Alert not existing'
        self.loger.info(msg)
        if raise_err_not_alert:
            raise NoSuchElementException(msg)

    def get_alert_text(self, time_out=5, raise_err=False) -> str:
        self.loger.info('Getting alert text')
        al = self.alert(time_out, raise_err)
        if al:
            return al.text
        else:
            return ''

    def accept_alert(self, time_out=5, raise_err=False):
        self.loger.info('Accepting alert')
        al = self.alert(time_out, raise_err)
        if al:
            al.accept()

    def dismiss_alert(self, time_out=5, raise_err=False):
        self.loger.info('Dismissing alert')
        al = self.alert(time_out, raise_err)
        if al:
            al.dismiss()

    def send_keys_alert(self, s, time_out=5, raise_err=False):
        self.loger.info(f'Inputting alert with "{s}"')
        al = self.alert(time_out, raise_err)
        if al:
            al.send_keys(s)


"""
mobile_emulation = {
            "deviceName": "Apple iPhone 3GS",
            "deviceName": "Apple iPhone 4",
            "deviceName": "Apple iPhone 5",
            "deviceName": "Apple iPhone 6",
            "deviceName": "Apple iPhone 6 Plus",
            "deviceName": "BlackBerry Z10",
            "deviceName": "BlackBerry Z30",
            "deviceName": "Google Nexus 4",
            "deviceName": "Google Nexus 5",
            "deviceName": "Google Nexus S",
            "deviceName": "HTC Evo, Touch HD, Desire HD, Desire",
            "deviceName": "HTC One X, EVO LTE",
            "deviceName": "HTC Sensation, Evo 3D",
            "deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black",
            "deviceName": "LG Optimus G",
            "deviceName": "LG Optimus LTE, Optimus 4X HD" ,
            "deviceName": "LG Optimus One",
            "deviceName": "Motorola Defy, Droid, Droid X, Milestone",
            "deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2",
            "deviceName": "Motorola Droid Razr HD",
            "deviceName": "Nokia C5, C6, C7, N97, N8, X7",
            "deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900",
            "deviceName": "Samsung Galaxy Note 3",
            "deviceName": "Samsung Galaxy Note II",
            "deviceName": "Samsung Galaxy Note",
            "deviceName": "Samsung Galaxy S III, Galaxy Nexus",
            "deviceName": "Samsung Galaxy S, S II, W",
            "deviceName": "Samsung Galaxy S4",
            "deviceName": "Sony Xperia S, Ion",
            "deviceName": "Sony Xperia Sola, U",
            "deviceName": "Sony Xperia Z, Z1",
            "deviceName": "Amazon Kindle Fire HDX 7″",
            "deviceName": "Amazon Kindle Fire HDX 8.9″",
            "deviceName": "Amazon Kindle Fire (First Generation)",
            "deviceName": "Apple iPad 1 / 2 / iPad Mini",
            "deviceName": "Apple iPad 3 / 4",
            "deviceName": "BlackBerry PlayBook",
            "deviceName": "Google Nexus 10",
            "deviceName": "Google Nexus 7 2",
            "deviceName": "Google Nexus 7",
            "deviceName": "Motorola Xoom, Xyboard",
            "deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1",
            "deviceName": "Samsung Galaxy Tab",
            "deviceName": "Notebook with touch",
            "deviceName": "iPhone 6"
}
"""
