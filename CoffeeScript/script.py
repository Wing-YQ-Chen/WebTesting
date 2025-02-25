import logging
import os.path
import traceback
import openpyxl
from Common.utils import *
from Common.openpyxl_common import set_value_to_range
from Common.web_ui_driver import WebUiDriver
from Common.log import setup_logging
from CoffeeScript.Pages.CartPage import CartPage
from CoffeeScript.Pages.MenuPage import MenuPage


class OrderScript:

    def __init__(self, url: str, input_data: dict, xl_report_path: str, screenshot_dir: str,
                 loger: logging.getLogger()):
        self.loger = loger
        self.input_data = input_data
        self.case_no = input_data['Case no.'].__str__().strip()
        self.case_status = ''
        self.case_msg = ''
        self.result = []
        self.url = url

        self.xl_report_path = os.path.abspath(xl_report_path)
        self.screenshot_dir = os.path.join(screenshot_dir, self.case_no)

        self.loger.info(f'case_number:{self.case_no}')
        self.loger.info(f'url:{self.url}')

    def order(self):
        wd = WebUiDriver(loger=self.loger)
        wd.get(self.url)
        mp = MenuPage(wd)
        cp = CartPage(wd)

        try:
            mp.select_product(self.input_data)
            mp.access_cart_page()
            wd.screenshot(self.screenshot_dir)
            capture_result = cp.capture_info()
            self.result.append(capture_result)
            cp.submit_payment(self.input_data)
            self.case_status = 'Success'
            self.case_msg = ''
        except BaseException as e:
            self.loger.error(traceback.format_exc())
            self.case_status = 'Failed'
            self.case_msg = e.__str__()
        wd.quit()

    def record_result(self):
        case_info = [self.case_no, self.case_status, self.case_msg,
                     f'=HYPERLINK(\"{self.screenshot_dir.replace("../Report", ".")}\", "Open screen folder")']
        case_info.extend(self.result)
        self.loger.info(f'Recording result\n{case_info}')
        report_wk = openpyxl.load_workbook(self.xl_report_path)
        report_ws = report_wk.worksheets[1]
        input_row = report_ws.max_row + 1
        set_value_to_range(report_ws, f"A{input_row}", case_info)
        report_wk.save(self.xl_report_path)
        report_wk.close()


"https://seleniumbase.io/demo_page/"

if __name__ == '__main__':
    input_data = {
        'Espresso_no': 1,
        'Espresso_Macchiato_no': 1,
        'Cappuccino_no': 1,
        'Mocha_no': 1,
        'Flat_White_no': 1,
        'Americano_no': 1,
        'Cafe_Latte_no': 1,
        'Espresso_Con_Panna_no': 1,
        'Cafe_Breve_no': 1,
        'name': 'Wing Test',
        'email': 'w@t.com',
        'receive checkbox': 'Yes'
    }

    OrderScript('debug.xlsx', r'.\debug_screens', setup_logging()).order(input_data)
    pass
