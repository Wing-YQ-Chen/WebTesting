from Common.web_ui_driver import WebBasicPage, WebUiDriver, ElmWith
from Common.log import setup_logging


class CartPage(WebBasicPage):
    total_btn = {ElmWith.XPATH: '//button[contains(text(),"Total")]'}
    name_input = {ElmWith.ID: 'name'}
    email_input = {ElmWith.ID: 'email'}
    receive_checkbox = {ElmWith.XPATH: '//input[@id="promotion"]'}
    submit_btn = {ElmWith.ID: 'submit-payment'}

    def capture_info(self):
        self.loger.info('capture_info')
        cart_table = []
        for row_no in range(1, self.webdriver.find_elements(
                ElmWith.XPATH, r'//div[@class="list"]/div/ul/li[@class="list-item"]', 'rows_elm').__len__()):
            row_elms = self.webdriver.find_elements(ElmWith.XPATH,
                                                    f'//div[@class="list"]/div/ul/li[@class="list-item"][{row_no}]/div')
            cart_table.append([row_elms[0].text, row_elms[1].text, row_elms[2].text])
        return self.webdriver(**self.total_btn).text

    def submit_payment(self, input_data: dict):
        self.loger.info('submit_payment')
        self.webdriver(**self.total_btn).click()
        self.webdriver(**self.name_input).send_keys(input_data.get('name'))
        self.webdriver(**self.email_input).send_keys(input_data.get('email'))
        self.webdriver(**self.receive_checkbox).tick_checkbox(
            True if 'Y' in input_data.get('receive checkbox').__str__() else False)
        self.webdriver(**self.submit_btn).click()
