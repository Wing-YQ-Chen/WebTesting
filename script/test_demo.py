import os.path
import traceback
import random

import pytest
import time
from Pages.DemoPage import DemoPage
from common.log import setup_logging
from common.web_ui_driver import WebUiDriver
from main import input_datas, report_folder, mark_report


@pytest.mark.parametrize("input_data", input_datas)
def test_demo(input_data):
    time.sleep(random.randint(0, 5))  # 临时解决方案：避免测试用例同时运行导致的问题
    case = input_data['case no.'].__str__()
    data = input_data['data'].__str__()
    log_dir_path = os.path.join(report_folder, 'log')
    screen_dir_path = os.path.join(report_folder, 'screen', case)

    loger, log_path = setup_logging(log_dir_path=log_dir_path, log_name=f'case {case}')
    loger.info(f'Testing for case {case}')
    try:
        driver = WebUiDriver()
        driver.get('https://seleniumbase.io/demo_page/')
        dp = DemoPage(driver)
        dp.input_demo_page(data)
        driver.screenshot(screen_dir_path)
        driver.quit()
        status = 'Success'
    except BaseException as e:
        loger.error(traceback.format_exc())
        status = 'Failed'

    loger.info(f'Case {case} done')
    # 获取loger文件的绝对路径
    loger = os.path.join(log_dir_path, f'case {case}.log')

    mark_report(case,
                status,
                f'=HYPERLINK(\"{os.path.abspath(screen_dir_path)}\", "Open screen folder")',
                f'=HYPERLINK(\"{os.path.abspath(log_path)}\", "Open log file")')
