"""
@desc: 日志模块底层设置相关
"""

import logging
import sys
from .logger_maker import logger, special_logger, init_handler, decorator_logger
from .logger_config import NOCOLOR_NORMAL_LOGGER_FORMAT
from .logger_utility import create_log_file, swap_logger_handlers, change_use_html


def set_logger(level: str = 'DEBUG', format_str: str = '', file_mode: bool = False, file_path: str = '',
               is_stdout=False, is_html=False):
    """
    设置日志格式
    :param level: 设置日志等级，仅能取[CRITICAL、ERROR、WARNING、INFO、DEBUG]中的一种
    :param format_str: 设置日志打印格式
    :param file_mode: 是否将日志写入文件，布尔值
    :param file_path: 日志文件路径，不填将自动生成日志文件
    :param is_stdout:
    :param is_html:
    :return:
    """
    try:
        change_use_html(is_html)
        level = level.upper()
        if level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            logger.setLevel(getattr(logging, level))
        else:
            logger.error('日志设置错误：level必须为[CRITICAL、ERROR、WARNING、INFO、DEBUG]')
        if format_str != '' or is_stdout:
            try:
                # 先删去原有格式
                logger.removeHandler(init_handler)
                # 构建格式
                fmt = init_handler.formatter if format_str == '' else logging.Formatter(format_str)
                # 设置格式再添加到logger上
                ch = logging.StreamHandler(sys.stdout) if is_stdout else logging.StreamHandler()

                if is_stdout:  # 把表格打印也加入到管道中
                    special_logger.removeHandler(special_logger.handlers)
                    special_logger.addHandler(ch)
                    special_logger.parent = None

                ch.setFormatter(fmt)
                logger.addHandler(ch)
            except Exception as e:
                logger.error(f'日志设置错误：请检查format_str参数格式{e}')
        if file_mode or file_path != '':
            # 如果没有指定文件目录，则在当前目录建立TestTech_log文件夹并以日期建立日志文件
            file_path = create_log_file(file_path)
            # 修改正常打印logger
            fh = logging.FileHandler(file_path, encoding='utf-8')
            fh.setFormatter(
                logging.Formatter(NOCOLOR_NORMAL_LOGGER_FORMAT if format_str == "" else format_str))
            logger.addHandler(fh)
            swap_logger_handlers(logger)
            # 修改特殊打印logger
            sfh = logging.FileHandler(file_path, encoding='utf-8')
            special_logger.addHandler(sfh)
            swap_logger_handlers(special_logger)
            # 修改装饰器打印logger
            decorator_logger.addHandler(sfh)
            swap_logger_handlers(decorator_logger)
    except Exception as e:
        print(e)
