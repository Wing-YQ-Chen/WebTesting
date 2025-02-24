import pytest
import threading
import sys, os

# 添加 common 模块所在的路径到 sys.path，否则终端运行时找不到common模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.openpyxl_common import *


def get_input():
    input_file_path = '../input/DemoInput.xlsx'
    report_dir_path = os.path.join('../Reports/DemoScript', get_timestamp_str())
    report_xl_path = create_report_xl(input_file_path, report_dir_path, 'Report', ['Report'])
    return extract_input_data(input_file_path), report_dir_path, report_xl_path


def mark_report(case, status, screen_path, log_path):
    report_lock.acquire(True)
    report_wk = openpyxl.load_workbook(report_xl_path)
    report_ws = report_wk.worksheets[0]
    input_row = report_ws.max_row + 1
    set_value_to_range(report_ws, f"A{input_row}", [case, status, screen_path, log_path])
    report_wk.save(report_xl_path)
    report_wk.close()
    report_lock.release()


report_lock = threading.Lock()
input_datas, report_folder, report_xl_path = get_input()

if __name__ == '__main__':
    pytest.main(['-n', '3'])
