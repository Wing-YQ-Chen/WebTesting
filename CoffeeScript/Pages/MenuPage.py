from Common.web_ui_driver import WebBasicPage, WebUiDriver, ElmWith
from Common.log import setup_logging


class MenuPage(WebBasicPage):
    Espresso_pd = {ElmWith.XPATH: '//h4[text()="Espresso "]/..//div', ElmWith.BIZ_NAME: 'Espresso'}
    Espresso_Macchiato_pd = {ElmWith.XPATH: '//h4[text()="Espresso Macchiato "]/..//div', ElmWith.BIZ_NAME: 'Espresso Macchiato'}
    Cappuccino_pd = {ElmWith.XPATH: '//h4[text()="Cappuccino "]/..//div', ElmWith.BIZ_NAME: 'Cappuccino'}
    Mocha_pd = {ElmWith.XPATH: '//h4[text()="Mocha "]/..//div', ElmWith.BIZ_NAME: 'Mocha'}
    Flat_White_pd = {ElmWith.XPATH: '//h4[text()="Flat White "]/..//div', ElmWith.BIZ_NAME: 'Flat White'}
    Americano_pd = {ElmWith.XPATH: '//h4[text()="Americano "]/..//div', ElmWith.BIZ_NAME: 'Americano'}
    Cafe_Latte_pd = {ElmWith.XPATH: '//h4[text()="Cafe Latte "]/..//div', ElmWith.BIZ_NAME: 'Cafe Latte'}
    Espresso_Con_Panna_pd = {ElmWith.XPATH: '//h4[text()="Espresso Con Panna "]/..//div', ElmWith.BIZ_NAME: 'Espresso Con Panna'}
    Cafe_Breve_pd = {ElmWith.XPATH: '//h4[text()="Cafe Breve "]/..//div', ElmWith.BIZ_NAME: 'Cafe Breve'}
    menu_tab_btn = {ElmWith.XPATH: '//*[contains(text(), "menu")]', ElmWith.BIZ_NAME: 'menu tab btn'}
    cart_tab_btn = {ElmWith.XPATH: '//*[contains(text(), "cart (")]', ElmWith.BIZ_NAME: 'cart tab btn'}

    def select_product(self, input_data: dict):
        self.webdriver(errmsg='Access menu page failed', **self.menu_tab_btn).click()
        if input_data.get('Espresso_no'):
            v = int(input_data.get('Espresso_no'))
            for i in range(0, v):
                self.webdriver(**self.Espresso_pd).click()
        if input_data.get('Espresso_Macchiato_no'):
            v = int(input_data.get('Espresso_Macchiato_no'))
            for i in range(0, v):
                self.webdriver(**self.Espresso_Macchiato_pd).click()
        if input_data.get('Cappuccino_no'):
            v = int(input_data.get('Cappuccino_no'))
            for i in range(0, v):
                self.webdriver(**self.Cappuccino_pd).click()
        if input_data.get('Mocha_no'):
            v = int(input_data.get('Mocha_no'))
            for i in range(0, v):
                self.webdriver(**self.Mocha_pd).click()
        if input_data.get('Flat_White_no'):
            v = int(input_data.get('Flat_White_no'))
            for i in range(0, v):
                self.webdriver(**self.Flat_White_pd).click()
        if input_data.get('Americano_no'):
            v = int(input_data.get('Americano_no'))
            for i in range(0, v):
                self.webdriver(**self.Americano_pd).click()
        if input_data.get('Cafe_Latte_no'):
            v = int(input_data.get('Cafe_Latte_no'))
            for i in range(0, v):
                self.webdriver(**self.Cafe_Latte_pd).click()
        if input_data.get('Espresso_Con_Panna_no'):
            v = int(input_data.get('Espresso_Con_Panna_no'))
            for i in range(0, v):
                self.webdriver(**self.Espresso_Con_Panna_pd).click()
        if input_data.get('Cafe_Breve_no'):
            v = int(input_data.get('Cafe_Breve_no'))
            for i in range(0, v):
                self.webdriver(**self.Cafe_Breve_pd).click()

    def access_cart_page(self):
        self.webdriver(**self.cart_tab_btn).click()
