from openpyxl.styles import *
# from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.service import Service

import os
import re

red_font = Font(name="DengXian", color="FF0000")
green_font = Font(name="DengXian", color="00B050")
orange_fill = PatternFill("solid", fgColor="E87722")
yellow_fill = PatternFill("solid", fgColor="FFFF00")


def get_timestamp_str(time_format: str = r'%Y%m%d%H%M%S'):
    # r'%Y/%m/%d %H:%M:%S'
    import time
    return time.strftime(time_format, time.localtime()).__str__()


def compare_str_num(left_v, right_v):
    left_v = left_v.__str__().strip()
    right_v = right_v.__str__().strip()
    re_is_number = r"^ *\d[\d\,\. ]*\d? *$"
    if re.search(re_is_number, left_v) and re.search(re_is_number, right_v):
        left_v = float(left_v.replace(" ", "").replace(",", ""))
        right_v = float(right_v.replace(" ", "").replace(",", ""))
        return left_v == right_v

    none_str = "None"
    none_list = [
        "",
        "None",
        "__ALIGNMENT__",
    ]

    if left_v in none_list: left_v = none_str
    if right_v in none_list: right_v = none_str
    return left_v == right_v


def compare_table(left_table, right_table, highlight_mode=1, re_ignore_list=[], equal_ignore_list=[]):
    """
    :param left_table:
    :param right_table:
    :param highlight_mode: 1 is orange background. 2 is highlight by red font.
    :param re_ignore_list / equal_ignore_list: no to compare if meet
    :return: a font/fill table for highlight in excel
    """
    total_compare = 0
    total_equals = 0
    highlight_table = list()

    max_row = left_table.__len__() if left_table.__len__() <= right_table.__len__() else right_table.__len__()
    max_col = left_table[0].__len__() if left_table[0].__len__() <= left_table[0].__len__() else left_table[0].__len__()
    for row in range(max_row):
        highlight_list = list()
        for col in range(max_col):
            total_compare += 1
            left_value = left_table[row][col].__str__().strip()
            right_value = right_table[row][col].__str__().strip()
            for re_ignore in re_ignore_list:
                if re.search(re_ignore, right_value, re.I):
                    highlight_list.append(yellow_fill)
                    break
            else:
                if right_value in equal_ignore_list:
                    highlight_list.append(yellow_fill)
                elif compare_str_num(left_value, right_value):
                    total_equals += 1
                    highlight_list.append(None)
                else:
                    temp_var = orange_fill
                    if highlight_mode == 2:
                        temp_var = red_font
                    highlight_list.append(temp_var)

        highlight_table.append(highlight_list)
    return highlight_table, round((total_equals / total_compare) * 100, 2) if total_compare > 0 else 0


def append_none_for_short_list(left_table, right_table, append_var):
    if left_table.__len__() >= right_table.__len__():
        for i in range(0, left_table.__len__() - right_table.__len__()):
            right_table.append(copy.deepcopy(append_var))
    else:
        for i in range(0, right_table.__len__() - left_table.__len__()):
            left_table.append(copy.deepcopy(append_var))
    return left_table, right_table


def path_list_filter_with_re(path_list, re_str):
    temp_var = []
    for i in range(0, path_list.__len__()):
        if re.search(re_str, path_list[i].__str__(), re.I):
            continue
        else:
            temp_var.append(path_list[i])
    return temp_var


def align_both_path_list(left_list, right_list, insert_var):
    """
    :param left_list:
    :param right_list:
    :param insert_var:
    :param replace_str:
    :return:
    """
    re_image_name = r"(?<=\_).*(?=\.[A-Za-z]{3})"
    for left_i in range(0, left_list.__len__()):
        left_name = os.path.basename(left_list[left_i])
        left_name = re.search(re_image_name, left_name)
        left_name = left_name.group() if left_name else left_name
        for right_i in range(0, right_list.__len__()):
            # match name then break
            right_name = os.path.basename(right_list[right_i])
            right_name = re.search(re_image_name, right_name)
            right_name = right_name.group() if right_name else right_name
            if left_name == right_name:
                if left_i != right_i:
                    temp_var = right_list[right_i]
                    right_list.pop(right_i)
                    right_list.insert(left_i, temp_var)
                break
        else:
            right_list.insert(left_i, copy.deepcopy(insert_var))

    for i in range(0, left_list.__len__() - right_list.__len__()):
        # for the duplicate key
        right_list.append(copy.deepcopy(insert_var))

    for i in range(0, right_list.__len__() - left_list.__len__()):
        left_list.append(copy.deepcopy(insert_var))

    return left_list, right_list


def align_both_table(left_table, right_table, key_column=0, re_key="", insert_none=[], replace_str=None):
    # for replace the replace_str to blank string
    for left_row in range(0, left_table.__len__()):
        left_key = left_table[left_row][key_column].__str__().strip()
        for right_row in range(0, right_table.__len__()):
            right_key = right_table[right_row][key_column].__str__().strip()
            if re_key:
                temp_var1 = re.search(re_key, left_key, re.I)
                temp_var2 = re.search(re_key, right_key, re.I)
                if temp_var1 and temp_var2:
                    left_key = temp_var1.group() if temp_var1 else left_key
                    right_key = temp_var2.group() if temp_var2 else right_key
            if left_key == right_key:
                if left_row != right_row:
                    temp_var = right_table[right_row]
                    right_table.pop(right_row)
                    right_table.insert(left_row, temp_var)
                break
        else:
            right_table.insert(left_row, copy.deepcopy(insert_none))

    for i in range(0, left_table.__len__() - right_table.__len__()):
        # for the duplicate key
        right_table.append(copy.deepcopy(insert_none))

    for i in range(0, right_table.__len__() - left_table.__len__()):
        left_table.append(copy.deepcopy(insert_none))

    if replace_str:
        for row in range(0, left_table.__len__()):
            for col in range(0, left_table[row].__len__()):
                if left_table[row][col].__str__() == replace_str: left_table[row][col] = ""

        for row in range(0, right_table.__len__()):
            for col in range(0, right_table[row].__len__()):
                if right_table[row][col].__str__() == replace_str: right_table[row][col] = ""

    return left_table, right_table


def get_name_from_hyperlink_formula(hyperlink_formula):
    temp_var = re.search(r'(?<=\, \").*(?=\")', hyperlink_formula)
    return temp_var.group() if temp_var else hyperlink_formula


def get_hyperlink_formula(path, text):
    return "=HYPERLINK(\"{}\", \"{}\")".format(path, text)


def get_link_from_onedrive_path(onedrive_path):
    if not os.path.exists(onedrive_path): return onedrive_path
    re_onedrive_base_path = r".*OneDrive - FWD Group Management Holdings Limited\\"
    # ondrive_base_link = r"https://fwdgroup-my.sharepoint.com/personal/pmohih_hk_fwd_com/Documents/"
    ondrive_base_link = r"https://fwdgroup-my.sharepoint.com/personal/gzowcn_hk_fwd_com/Documents/"
    ondrive_link = re.sub(re_onedrive_base_path, ondrive_base_link, onedrive_path)
    ondrive_link = re.sub(r"\\", r"/", ondrive_link)
    ondrive_link = re.sub(r" ", r"%20", ondrive_link)
    return ondrive_link


def get_yaml_data(yaml_path):
    yaml_file = open(yaml_path, 'r', encoding="utf-8")
    yaml_str = yaml_file.read()
    yaml_file.close()
    return yaml.load(yaml_str)


def get_random_number(number_length: int) -> int:
    from faker import Faker
    return Faker(locale='zh_CN').random_number(number_length, fix_len=True)


def delete_proxy(path):
    import os
    logger.info(f"Deleting Proxy")
    os.system(f'"{path}"')


def send_outlook_email(to: list, subject: str, html_body: str, attachment_path: str = ''):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = ';'.join(to)
    mail.Subject = subject
    mail.HTMLBody = html_body
    if attachment_path:
        mail.Attachments.Add(attachment_path)
    mail.Send()


if __name__ == '__main__':
    # from loguru import logger
    # import loguru
    #
    # username = os.getlogin()
    # # log_path = os.path.join(log_dir_path, username + " {time}.log")
    # logger.add('.', format=r'{time:YYYY-MM-DD HH:mm:ss} | {file}-{line} | {level} | {message}', level=level, encoding="utf-8")
    import pandas as pd

    df1 = pd.read_csv(r'C:\Users\GZOWCN\Downloads\OneDrive_2024-08-29\ZRTRPF.csv', encoding='latin1')
    df2 = pd.read_csv(r'C:\Users\GZOWCN\Downloads\OneDrive_2024-08-29\ZRTRPF.csv', encoding='latin1')
    t = df1.values
    ct, so = compare_table(df1.values, df2.values)
    pass
