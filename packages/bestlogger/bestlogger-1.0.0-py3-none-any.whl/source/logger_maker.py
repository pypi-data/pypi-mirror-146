try:
    from .logger_rf import RobotLogger
except Exception as e:
    print(e)
    print('请安装依赖：pip install robotframework')
import logging
from .logger_color import ColoredFormatter, formatter_message
from .logger_config import NORMAL_LOGGER_FORMAT, NOCOLOR_NORMAL_LOGGER_FORMAT
from .logger_utility import create_log_file, swap_logger_handlers
from logging.handlers import RotatingFileHandler
import sys
import os
os.system('')


def get_logger(name, level, format_str, iscolor=False, is_stdout=False):
    color_formatter = ColoredFormatter(formatter_message(format_str, iscolor), iscolor)
    sh = logging.StreamHandler(sys.stdout) if is_stdout else logging.StreamHandler()
    sh.setFormatter(color_formatter)
    temp_logger = logging.getLogger(name)
    temp_logger.addHandler(sh)
    temp_logger.setLevel(level)
    return temp_logger, sh


global is_robot

robot_logger = RobotLogger()
# 判断当前是否在RF中
if robot_logger.EXECUTION_CONTEXTS.current is None and "performance_test" not in sys.path:
    # 正常打印logger
    logger, init_handler = get_logger('root', logging.DEBUG, NORMAL_LOGGER_FORMAT, True)
    # 对warn增加别名以解决warn使用时的提示问题
    logger.warn = logger.warning
    logger.parent = None
    is_robot = False
    # 装饰器打印logger
    decorator_logger, _ = get_logger('decorator', logging.DEBUG, '[%(asctime)s] - [%(levelname)s] %(message)s', True)
    decorator_logger.parent = None  # 将所有logger去除parent，避免多次打印log
    # 特殊打印logger
    # 修复表格打印时不对齐问题
    special_logger = logging.getLogger('special')
    special_logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    special_logger.addHandler(ch)
    # special_logger, _ = get_logger('special', logging.DEBUG, '', True)
    special_logger.parent = None
else:
    logger = robot_logger
    decorator_logger = robot_logger
    special_logger = robot_logger
    init_handler = None
    is_robot = True


def get_my_logger(name, level='DEBUG', format_str=NORMAL_LOGGER_FORMAT, file_mode: bool = False, file_path: str = '',
                  iscolor=True, isrobot=False, max_bytes=100, is_stdout=False):
    # 判断当前是否在RF中
    if robot_logger.EXECUTION_CONTEXTS.current is not None and isrobot:
        return robot_logger
    level = level.upper()
    if level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
        logger.error('日志设置错误：level必须为[CRITICAL、ERROR、WARNING、INFO、DEBUG]')
    if is_robot:
        temp_logger, _ = get_logger(name, level, NOCOLOR_NORMAL_LOGGER_FORMAT, False, is_stdout)
    else:
        temp_logger, _ = get_logger(name, level, format_str, iscolor, is_stdout)
    if file_mode:
        # 如果没有指定文件目录，则在当前目录建立TestTech_log文件夹并以日期建立日志文件
        file_path = create_log_file(file_path)
        # 修改正常打印logger
        fh = RotatingFileHandler(file_path, mode='a', maxBytes=max_bytes * 1024 * 1024, backupCount=2, encoding='utf-8')
        # fh = logging.FileHandler(file_path, encoding='utf-8')
        fh.setFormatter(
            logging.Formatter(
                NOCOLOR_NORMAL_LOGGER_FORMAT if format_str == "" or format_str == NORMAL_LOGGER_FORMAT else format_str))
        temp_logger.addHandler(fh)
        # 将两个handlers互相交换，否则颜色打印会影响到日志文件写入，产生乱码
        swap_logger_handlers(temp_logger)
    return temp_logger
