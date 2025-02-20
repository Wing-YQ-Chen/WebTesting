import os.path
import traceback

from Pages.DemoPage import DemoPage
from common.log import setup_logging
from common.web_ui_driver import WebUiDriver
from main import input_datas, report_folder, mark_report
import pytest


@pytest.mark.parametrize("input_data", input_datas)
def test_demo(input_data):
    case = input_data['case no.'].__str__()
    data = input_data['data'].__str__()
    log_dir_path = os.path.join(report_folder, 'log')
    screen_dir_path = os.path.join(report_folder, 'screen', case)

    loger = setup_logging(log_dir_path=log_dir_path, log_name=f'case {case}')
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

    mark_report(case,
                status,
                f'=HYPERLINK(\"{os.path.abspath(screen_dir_path)}\", "Open screen folder")',)
