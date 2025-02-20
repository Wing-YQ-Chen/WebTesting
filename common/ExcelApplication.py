# @Author: Wing Chen
# @Description: VBA
# @Last update on 2022/01/18

import win32com.client
import os
from openpyxl.styles import Font, colors, Alignment, PatternFill

# Default Color Index as per 18.8.27 of ECMA Part 4
COLOR_INDEX = (
    '00000000', '00FFFFFF', '00FF0000', '0000FF00', '000000FF',  # 0-4
    '00FFFF00', '00FF00FF', '0000FFFF', '00000000', '00FFFFFF',  # 5-9
    '00FF0000', '0000FF00', '000000FF', '00FFFF00', '00FF00FF',  # 10-14
    '0000FFFF', '00800000', '00008000', '00000080', '00808000',  # 15-19
    '00800080', '00008080', '00C0C0C0', '00808080', '009999FF',  # 20-24
    '00993366', '00FFFFCC', '00CCFFFF', '00660066', '00FF8080',  # 25-29
    '000066CC', '00CCCCFF', '00000080', '00FF00FF', '00FFFF00',  # 30-34
    '0000FFFF', '00800080', '00800000', '00008080', '000000FF',  # 35-39
    '0000CCFF', '00CCFFFF', '00CCFFCC', '00FFFF99', '0099CCFF',  # 40-44
    '00FF99CC', '00CC99FF', '00FFCC99', '003366FF', '0033CCCC',  # 45-49
    '0099CC00', '00FFCC00', '00FF9900', '00FF6600', '00666699',  # 50-54
    '00969696', '00003366', '00339966', '00003300', '00333300',  # 55-59
    '00993300', '00993366', '00333399', '00333333',  # 60-63
)
BLACK = COLOR_INDEX[0]
WHITE = COLOR_INDEX[1]
RED = COLOR_INDEX[2]
DARKRED = COLOR_INDEX[8]
BLUE = COLOR_INDEX[4]
DARKBLUE = COLOR_INDEX[12]
GREEN = COLOR_INDEX[3]
DARKGREEN = COLOR_INDEX[9]
YELLOW = COLOR_INDEX[5]
DARKYELLOW = COLOR_INDEX[19]


def update_output_file(output_file_path, content_list):
    output_ea = ExcelApplication(output_file_path, 1, output_file_path)
    row_number = output_ea.get_range_location('AA65536', end_1=output_ea.endUp)[0] + 1


class ExcelApplication(object):

    def __init__(self, excel_path: str, sheet=None, save_path='', is_close=True):
        """
        :param excel_path:
    output_ea.setValueToRange(content_list, 'AA' + row_number.__str__())
    del output_ea
        :param sheet: sheet name or sheet index number
        :param save_path: whether save workbook
        :param is_close: whether close workbook
        """
        if not os.path.exists(excel_path):
            raise FileNotFoundError('it can not find the excel file from path - ' + excel_path)

        self.is_close = is_close
        self.excel_path = excel_path
        self.save_path = save_path
        self.readOnly = True if save_path.__eq__('') or not excel_path.__eq__(save_path) else False
        self.readOnly = False
        self.application = win32com.client.Dispatch('Excel.Application')
        self.application.DisplayAlerts = False
        self.application.ScreenUpdating = False
        self.excelObject = self.application.Workbooks.Open(self.excel_path, False, self.readOnly)
        self.sheetObject = None
        if sheet is not None:
            self.setSheet(sheet)

        self.endUp = -4162
        self.endDown = -4121
        self.endLeft = -4159
        self.endRight = -4161

    def run_macro(self, macro_name):
        self.application.Run(macro_name)  # 貌似沒有返回值

    def setSheet(self, sheet):
        """
        :param sheet: sheet name or sheet index number
        :return: A worksheet object or None
        """
        if type(sheet) is str:
            for tempSheet in self.excelObject.Sheets:
                if tempSheet.Name.__eq__(sheet):
                    self.sheetObject = tempSheet
                    break
            else:
                # raise ValueError('There is not existing a sheet name is the ' + sheet)
                self.sheetObject = None
        elif type(sheet) is int:
            self.sheetObject = self.excelObject.Sheets(sheet)
        return self.sheetObject

    def getRange(self, cell_1, cell_2=None, end_1=None, end_2=None, sheet=None):
        """
        :param cell_1:
        :param cell_2:
        :param end_1:
        :param end_2:
        :param sheet: sheet name or sheet index number
        :return: A Range object or None
        """
        if sheet is not None:
            self.setSheet(sheet)

        if self.sheetObject:
            if end_1 is None:
                cell_1 = self.sheetObject.Range(cell_1)
            else:
                cell_1 = self.sheetObject.Range(cell_1).End(end_1)

            if cell_2 is None:
                return cell_1
            else:
                if end_2 is None:
                    cell_2 = self.sheetObject.Range(cell_2)
                else:
                    cell_2 = self.sheetObject.Range(cell_2).End(end_2)
                return self.sheetObject.Range(cell_1, cell_2)
        else:
            return None

    def getValueFromRange(self, cell_1, cell_2=None, end_1=None, end_2=None):
        return self.getRange(cell_1, cell_2, end_1, end_2).Value

    def getTextFromRange(self, cell_1, cell_2=None, end_1=None, end_2=None):
        return self.getRange(cell_1, cell_2, end_1, end_2).Text

    def get_range_location(self, cell_1, cell_2=None, end_1=None, end_2=None):
        rg = self.getRange(cell_1, cell_2, end_1, end_2)
        return [rg.Row, rg.Column]

    def setValueToRange(self, value, cell_1):
        """
        :param value: 暂只支持一维列表
        :param cell_1:
        :return:
        """
        if type(value) is list or type(value) is tuple:
            list_len = value.__len__()
        else:
            list_len = 0
        rg = self.getRange(cell_1)
        self.sheetObject.Range(rg, rg.Offset(1, list_len)).Value = value

    def __del__(self):
        if self.excel_path.__eq__(self.save_path):
            self.excelObject.Save()
        elif not self.save_path.__eq__(''):
            self.excelObject.SaveAs(self.save_path, 51)
        self.excelObject.Saved = True
        if self.is_close:
            self.excelObject.Close()
        self.application.DisplayAlerts = True
        self.application.ScreenUpdating = True
        # self.application.Quit()


if __name__ == '__main__':
    pass
