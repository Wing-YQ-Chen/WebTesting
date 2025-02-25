import copy
import os.path
import queue
import traceback
import openpyxl
import glob
import sys
import multiprocessing
import threading
# 添加 common 模块所在的路径到 sys.path，否则pytest在终端运行时找不到common模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Common.openpyxl_common import *
from Common.utils import *
from Common.log import setup_logging
from CoffeeScript.script import OrderScript



class Main:

    def __init__(self):
        self.report_path = None
        self.screenshot_dir = None
        self.lock = None
        self.runner_no = None
        self.url = None
        self.input_file_path = None
        self.input_table_q = queue.Queue()
        self.input_file_search_str = os.path.abspath('../*/Coffee_input.xlsx')
        self.report_dir = os.path.abspath('../Reports/Coffee_Demo')
        self.log_path = os.path.join(self.report_dir, 'Logs')

        self.loger, self.logfile_path = setup_logging(self.log_path)
        self.loger.info(f"log path: {self.log_path}")
        self.loger.info(f"Runner: {os.getlogin()}")

        self.get_input_data()
        self.set_up_output_file()

    def get_input_data(self):
        self.loger.info('================== Finding input file. ==================')
        self.input_file_path = glob.glob(self.input_file_search_str)
        if not self.input_file_path:
            self.loger.error(f'Not found the input file from below path\n{self.input_file_search_str}')
            return
        self.input_file_path = self.input_file_path[0]
        self.loger.info(f'Got the input file from below path\n{self.input_file_path}')

        self.loger.info('================== Reading input file ==================')
        input_wk = openpyxl.load_workbook(self.input_file_path, True)
        enviro_ws = input_wk.worksheets[1]
        self.url = enviro_ws["B1"].value.__str__().strip()
        self.runner_no = int(enviro_ws["B2"].value)
        input_wk.close()
        self.input_table_q = extract_input_data(self.input_file_path)
        if self.input_table_q.empty():
            self.loger.error('Input file is blank. Please check.')
            sys.exit()

    def set_up_output_file(self):
        self.loger.info('================== Creating output files ==================')
        self.screenshot_dir = os.path.join(self.report_dir, 'Screenshots', get_timestamp_str())
        self.report_path = create_report_xl(
            self.input_file_path, self.report_dir, "Demo_report", ['Input cases', 'Report'])

    def start_threading(self):
        self.loger.info('================== Creating Multi Threading ==================')
        self.lock = threading.Lock()

        td_list = []
        for _ in range(self.runner_no):
            td = threading.Thread(target=self.execute)
            td_list.append(td)
            td.start()

        for td in td_list:
            td.join()

        self.loger.info(f'========================== All cases execution done ==========================')

    def execute(self):
        loger, logfile_path = setup_logging(self.log_path)
        try:
            while True:
                try:
                    input_data = self.input_table_q.get(False)
                except BaseException:
                    self.loger.info(f'========================== END ==========================')
                    return
                loger.info(f'========================== RUNNING ==========================')
                loger.info(f'current_process:{multiprocessing.current_process().name}')
                loger.info(f'current_thread:{threading.current_thread().name}')
                ost = OrderScript(self.url, input_data, self.report_path, self.screenshot_dir, loger)
                ost.order()
                try:
                    self.lock.acquire()
                    ost.record_result()
                except BaseException:
                    self.loger.error(traceback.format_exc())
                finally:
                    self.lock.release()
        except BaseException:
            loger.error(
                f"{multiprocessing.current_process().name} {threading.current_thread().name} \n"
                f"Program end as encounter unknown error\n"
                f"{traceback.format_exc()}")


if __name__ == '__main__':
    main = Main()
    main.start_threading()

"""
==============================================================
脚本驱动层：通过控制输入输出文件和线程数，通过数据去驱动业务脚本层
==============================================================
业务脚本层：调用PO层的接口，根据业务逻辑，控制页面的执行顺序
==============================================================
页面脚本层：调用UI驱动层接口，让页面有序的动起来
==============================================================
UI 驱动层：提供让页面动起来的接口
==============================================================
"""
