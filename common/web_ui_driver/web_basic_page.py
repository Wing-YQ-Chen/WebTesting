from .web_ui_driver import WebUiDriver


class WebBasicPage(object):
    """
    PO 模型基础类
    """

    def __init__(self, webdriver: WebUiDriver):
        self.webdriver = webdriver
        self.loger = self.webdriver.loger
