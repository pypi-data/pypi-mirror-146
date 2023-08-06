import os
import time

_use_html = False


def change_use_html(flag):
    global _use_html
    _use_html = flag


def get_use_html():
    return _use_html


def create_log_file(log_dir=''):
    if log_dir == '' or os.path.isdir(log_dir):
        base_path = log_dir if log_dir != '' else './TestTech_log'
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        file_path = os.path.join(base_path, time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log')
        return file_path
    else:  # 否则可能为不存在路径或者文件
        if os.path.isfile(log_dir):
            return log_dir  # 如果是已存在文件路径则直接使用
        # 判断是文件夹路径还是文件路径，假设最后一段内容带有点，则认为是文件
        path_list = os.path.split(log_dir)
        if '.' in path_list[-1]:
            # 是文件的情况
            temp_dir = ''.join(path_list[:-1])
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            return os.path.join(temp_dir, path_list[-1])
        else:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            file_path = os.path.join(log_dir, time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log')
            return file_path


def swap_logger_handlers(input_logger):
    """
    需要将两个handlers互相交换，否则颜色打印会影响到日志文件写入，产生乱码。
    :param input_logger:
    :return:
    """
    input_logger.handlers[0], input_logger.handlers[1] = input_logger.handlers[1], input_logger.handlers[0]
