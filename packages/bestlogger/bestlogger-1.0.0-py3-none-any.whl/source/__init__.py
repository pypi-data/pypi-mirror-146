from .logger_maker import logger, get_my_logger
from .logger_decorator import log, catch, log_runtime
from .logger_method import split_line, verify_log, db_format_log, mark_as_case
from .logger_setting import set_logger


__version__ = "1.0.0"
__name__ = "berrerlogger"

__all__ = ["logger", "log", "catch", "split_line", "set_logger", "verify_log", "db_format_log", "mark_as_case",
           "get_my_logger", "log_runtime"]
