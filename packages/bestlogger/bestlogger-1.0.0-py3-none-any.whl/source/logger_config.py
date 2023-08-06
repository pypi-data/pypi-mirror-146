"""
@desc: 日志模块配置
"""

NORMAL_LOGGER_FORMAT = '[$YELLOW%(asctime)s$RESET] $GREEN%(filename)s$RESET->$GREEN%(funcName)s$RESET ' \
                       'line:$GREEN%(lineno)d$RESET [%(levelname)s] %(message)s'
NOCOLOR_NORMAL_LOGGER_FORMAT = '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s'
DECORATOR_LOG_FORMAT = '{0}: parameter:[{1}] | return:[{2}]'
DECORATOR_CATCH_FORMAT = '{0} 出错：{1}'
