"""
@desc: 日志模块普通方法
"""

import time
from .logger_maker import special_logger, is_robot, logger
from .logger_utility import get_use_html
import prettytable as pt
import sys


def split_line(item: str = '-', msg: str = '', timestamp: bool = False):
    """
    打印分割线
    :param item: 分割线的形式
    :param msg: 需要附加的信息
    :param timestamp: 是否添加时间戳
    :return:
    """
    if timestamp:
        stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if msg != '':
            msg = stamp + '：' + msg
        else:
            msg = stamp
    if len(msg) < 100:
        makeup = int(((100 - len(msg)) / 2)) * item
        msg = makeup + msg + makeup
    else:
        msg = item * 100
    special_logger.info(msg)


def verify_log(result, chinese_name=None, print_mode='all', is_rf_print=False):
    """
    打印比对表格
    :param result:
    :param print_mode:
    :param chinese_name:
    :param is_rf_print: 在RF环境下，是否打印日志中的表格
    :return:
    """
    try:
        sorted_dict = {False: 1, True: 2, 'Ignore': 3}
        result = sorted(result, key=lambda x: sorted_dict[x['result']])
    except Exception as e:
        print(e)
    if print_mode == 'all':
        print_mode = [True, False, 'Ignore']
    elif print_mode:
        print_mode = [True]
    elif not print_mode:
        print_mode = [False]
    elif print_mode == 'all_true_skip':
        print_mode = [True, False, 'Ignore']
        # 这种模式下，全对不打印
        if len([x for x in result if not x['result']]) == 0:
            return
    elif not print_mode:
        return
    color_dict = {True: 'forestgreen', False: 'firebrick', 'Ignore': 'Silver'}
    column_dict = {'real_val': '实际值', 'except_val': '预期值', 'result': '比对结果', 'key_name': '字段名',
                   'mapping_name': '映射字段名', 'chinese_name': '中文字段名'}
    if chinese_name:
        template_dict = ['key_name', 'chinese_name', 'real_val', 'except_val', 'result']
        # 如果传入中文字段名字典，则在结果中插入中文字段名
        for temp_dic in result:
            if temp_dic['key_name'] in chinese_name:
                temp_dic['chinese_name'] = chinese_name[temp_dic['key_name']]
            else:
                temp_dic['chinese_name'] = ' '
    elif 'key_name' in result[0]:
        template_dict = ['key_name', 'real_val', 'except_val', 'result']
        if 'mapping_name' in result[0]:
            template_dict.insert(2, 'mapping_name')
    else:
        template_dict = ['real_val', 'except_val', 'result']
    if is_robot or get_use_html():
        if len([x for x in result if x['result'] in print_mode]) > 0:  # 打印内容不为空的时候才打印
            row_template = u'<tr><td><pre style="border-radius:5px;font-family:宋体;color:white;margin:0;padding:5px;' \
                           u'background-color:black">{}</pre></td>{}</tr>'
            cell_template = u'<td><pre style="border-radius:5px;font-family:宋体;color:white;margin:0;padding:5px;' \
                            u'background-color:{}">{}</pre></td>'
            data = u'<div style="overflow-y:auto"><table style="word-break:keep-all"><tbody>{}</tbody></table></div>' \
                .format(u"".join(row_template.format(column_dict[i], u"".join(
                    cell_template.format(color_dict[item['result']] if '名' not in column_dict[i] else 'Silver',
                                         ' ' if item[i] == '' else item[i]) for item
                    in
                    result if item['result'] in print_mode)
                                                     ) for i in template_dict))
            logger.info(data, html=True) if is_robot else logger.info(data)
    if not is_robot or (is_robot and is_rf_print):
        # 非robor环境下，使用原生log打印方式
        tb = pt.PrettyTable(result[0].keys())
        for info in result:
            if info['result'] in print_mode:
                tb.add_row([x.strip() if type(x) == str else x for x in info.values()])
        if len(tb._rows) > 0:  # 打印内容不为空的时候才打印
            special_logger.info(tb)


def db_format_log(json_list, chinese_name: dict = None):
    """
    用于打印列表嵌套字典内容
    :param json_list:
    :param chinese_name:
    :return:
    """
    if len(json_list) == 0:
        # logger.warn('数据库查询结果为空！')
        return None
    try:
        if is_robot or get_use_html():
            # 如果在RF中，需要提前对数据进行转换
            all_data_list = []
            columns = json_list[0].keys()
            all_data_list.append(columns)
            if chinese_name:
                chinese_name_list = []
                for column in columns:
                    chinese_name_list.append(chinese_name[column])
                all_data_list.append(chinese_name_list)
            for j in json_list:
                temp_data = []
                for key in columns:
                    temp_data.append(j[key])
                all_data_list.append(temp_data)

            row_template = u'<tr><td><pre style="border-radius:5px;font-family:宋体;color:white;margin:0;padding:5px;' \
                           u'background-color:white"></pre></td>{}</tr>'
            cell_template = u'<td><pre style="border-radius:5px;font-family:宋体;color:white;margin:0;padding:5px;' \
                            u'background-color:CornflowerBlue">{}</pre></td>'
            data = u'<div style="overflow-y:auto"><table style="word-break:keep-all"><tbody>{}</tbody></table></div>'\
                .format(u"".join(row_template.format(u"".join(
                    cell_template.format(' ' if item == '' else item) for item in data_list)
                ) for data_list in all_data_list))
            logger.info(data, html=True) if is_robot else logger.info(data)
        else:
            # 非robor环境下，使用原生log打印方式
            tb = pt.PrettyTable(json_list[0].keys())
            columns = json_list[0].keys()
            try:
                if chinese_name:  # 数据库查询中文名字典
                    chinese_name_list = [chinese_name[x] for x in columns]
                    tb.add_row(chinese_name_list)
            except Exception as e:
                print(e)
            for info in json_list:
                info_list = [info[x] for x in columns]
                tb.add_row(info_list)
            special_logger.info(tb)
    except Exception as e:
        print(e)


def mark_as_case(flag: bool):
    flag = 'SUCCESS' if flag else 'FAIL'
    logger.info('[{}]  RF在线平台数据驱动案例标识_{}'.format(sys._getframe().f_back.f_lineno, flag))
