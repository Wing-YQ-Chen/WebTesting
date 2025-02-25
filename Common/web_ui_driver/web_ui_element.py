import logging
import time
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


class ElmWith(object):
    """
    元素信息类，配合find_element
    """
    BIZ_NAME = 'biz_name'
    ID = By.ID
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    NAME = By.NAME
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME
    CSS_SELECTOR = By.CSS_SELECTOR
    TIMEOUT = 'timeout'
    IGNORE_ERR = 'ignore_err'
    ERRMSG = "errmsg"

class WebUiElement(WebElement):
    """
    WebUiElement类继承自WebElement，用于对网页元素进行更丰富的操作，同时提供了日志记录功能。
    这个类主要是为了方便在自动化测试或其他与网页交互的场景中使用。
    """

    def __init__(self, webdriver, id_, loger=logging.getLogger(), biz_name='') -> None:
        """
        初始化WebUiElement对象。

        :param webdriver: 驱动程序对象，用于控制浏览器。
        :param id_: 网页元素的标识符。
        :param loger: 日志记录器对象，默认为根日志记录器。
        :param biz_name: 业务名称，用于在日志中标识操作的元素所属业务，默认为空字符串。
        """
        from .web_ui_driver import WebUiDriver
        self.loger = loger
        self.biz_name = biz_name
        self.webdriver: WebUiDriver = webdriver
        super().__init__(webdriver, id_)

    def click(self) -> None:
        """
        点击网页元素，并在日志中记录点击操作信息，包括业务名称。
        """
        self.loger.info(f'🖱️ Click for {self.biz_name}')
        super().click()

    def js_click(self) -> None:
        """
        使用JavaScript执行点击网页元素的操作，并在日志中记录相关信息。
        这种方式可能在某些情况下比普通的click方法更可靠。
        """
        self.loger.info(f'🖱️ JS Click for {self.biz_name}')
        self.webdriver.execute_script("arguments[0].click();", self)

    def clear(self) -> None:
        """
        清除网页元素的内容，并在日志中记录清除操作信息，包括业务名称。
        此方法调用父类（WebElement）的clear方法。
        """
        self.loger.info(f'🚿 Clear for {self.biz_name}')
        super().clear()

    def js_clear(self) -> None:
        """
        使用JavaScript清除网页元素的内容，并在日志中记录相关信息。
        它通过设置元素的value属性为空来实现清除。
        """
        self.loger.info(f'🚿 JS Clear for {self.biz_name}')
        self.webdriver.execute_script("arguments[0].value = '';", self)

    def send_keys(self, value: str or None, clear: bool = True) -> None:
        """
        向网页元素输入内容。

        :param value: 要输入的字符串值，如果为None则不进行输入操作。
        :param clear: 是否在输入前清除元素内容，默认为True。
        首先记录输入操作的日志信息，包括要输入的值和业务名称。
        如果有值要输入且需要清除内容，则先调用js_clear方法清除，然后使用父类的send_keys方法输入内容。
        """
        self.loger.info(f'🎹 Input {value} to {self.biz_name}')
        if value:
            if clear:
                self.js_clear()
            super().send_keys(value)

    def tick_checkbox(self, y_or_n: bool):
        """
        勾选或取消勾选复选框。

        :param y_or_n: 布尔值，表示是否勾选。True为勾选，False为取消勾选。
        首先记录操作复选框的日志信息，包括要设置的状态和业务名称。
        然后获取复选框当前的选中状态，如果与目标状态不一致，则通过发送空格来切换状态。
        """
        logging.info(f"✅ Tick checkbox to {y_or_n} for {self.biz_name}")
        elm_status = self.is_selected()
        if elm_status != y_or_n:
            super().send_keys(' ')

    def get_action_chains(self) -> ActionChains:
        """
        获取一个用于操作当前网页元素的动作链（ActionChains）对象。
        动作链可用于执行一系列复杂的鼠标操作。
        """
        return ActionChains(self.webdriver)

    def mouse_hover(self):
        """
        将鼠标悬停在当前网页元素上。
        通过获取动作链并执行move_to_element操作来实现。
        """
        self.get_action_chains().move_to_element(self).perform()

    def drag_to(self, target_element: 'WebUiElement'):
        """
        将当前网页元素拖曳到目标网页元素上。
        通过获取动作链并执行drag_and_drop操作来实现。
        :param target_element: 目标网页元素，即要拖曳到的位置。
        """
        self.get_action_chains().drag_and_drop(self, target_element).perform()

    def get_select_object(self) -> Select:
        """
        获取当前网页元素对应的Select对象，用于操作下拉列表。
        """
        return Select(self)

    def select(self, option_value: int or str):
        """
        在下拉列表中选择指定的值或索引对应的选项。

        :param option_value: 要选择的选项的值或索引，可以是整数（索引）或字符串（值）。
        首先获取Select对象。
        如果option_value为None，则取消选择所有选项（对于支持多选的下拉列表）。
        否则，根据option_value的类型（整数或字符串），使用相应的选择方法（select_by_index或select_by_value）。
        同时在日志中记录选择操作的信息，包括选择的值和业务名称。
        """
        s = self.get_select_object()
        if option_value is None:
            logging.info(f"🎨 Deselecting for list {self.biz_name}")
            s.deselect_all()
        else:
            logging.info(f"🎨 Selecting {option_value} option from list {self.biz_name}")
            if type(option_value) is int:
                s.select_by_index(option_value)
            else:
                s.select_by_visible_text(option_value)

    def scroll_to_view(self) -> None:
        """
        将当前网页元素滚动到可见区域，并在日志中记录滚动操作信息，包括业务名称。
        通过执行JavaScript的scrollIntoView方法来实现。
        """
        logging.info(f"🛴 Scroll to elem {self.biz_name}")
        self.webdriver.execute_script("arguments[0].scrollIntoView();", self)

    def __set_border(self, px: int = 2) -> None:
        """
        设置当前网页元素的边框样式。

        :param px: 边框宽度，默认为2像素。
        尝试设置边框样式，如果px大于0，则设置为红色边框，否则清除边框样式。
        如果出现异常则忽略（可能是由于某些元素不支持设置边框样式）。
        """
        try:
            style_red = f'arguments[0].style.border="{px}px solid #FF0000"'
            style_null = 'arguments[0].style.border=""'
            if px:
                self.webdriver.execute_script(style_red, self)
            else:
                self.webdriver.execute_script(style_null, self)
        except BaseException:
            pass

    def highlight(self, px: int = 2) -> None:
        """
        高亮显示当前网页元素，即设置红色边框，短暂停留后清除边框。

        :param px: 边框宽度，默认为2像素。
        通过调用__set_border方法来设置和清除边框，实现高亮效果。
        停留0.1秒后清除边框，使元素恢复原状。
        """
        self.__set_border(px)
        time.sleep(0.1)
        self.__set_border(0)

    @property
    def get_value(self):
        """
        获取当前网页元素的value属性值。
        此属性可用于获取输入框、下拉列表等元素的当前值。
        """
        return self.get_attribute('value')
