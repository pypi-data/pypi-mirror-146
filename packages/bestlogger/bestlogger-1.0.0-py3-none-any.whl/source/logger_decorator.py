"""
日志模块装饰器相关
"""
import traceback
from .logger_maker import decorator_logger
from .logger_config import DECORATOR_CATCH_FORMAT, DECORATOR_LOG_FORMAT
import functools
import time
import sys


def log(func):
    @functools.wraps(func)
    def wrapper(*arg, **kw):
        dic = {}
        # 默认输入参数
        for index, item in enumerate(arg):
            dic[func.__code__.co_varnames[index]] = item
        # 带形参输入参数
        for key, value in kw.items():
            dic[key] = value
        msg = DECORATOR_LOG_FORMAT
        result = func(*arg, **kw)
        decorator_logger.info(msg.format(func.__name__, dic, result))
        return result

    return wrapper


def catch(is_continue=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*arg, **kw):
            try:
                result = func(*arg, **kw)
                return result
            except Exception as e:
                msg = DECORATOR_CATCH_FORMAT
                decorator_logger.error(msg.format(func.__name__, e))
                if is_continue:
                    traceback.print_exc()
                else:
                    # raise e
                    et, ei, tb = sys.exc_info()
                    decorator_logger.error('错误堆栈：\n'+''.join(traceback.format_tb(tb)[1:]))
                    sys.exit(0)
        return wrapper

    return decorator


def log_runtime(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        decorator_logger.info('方法：[%s] 运行耗时： %.2f' % (func.__name__, time.time() - local_time))

    return wrapper


class StackTrace(object):
    def __init__(self, with_call=True, with_return=False,
                 with_exception=False, max_depth=-1):
        self._frame_dict = {}
        self._options = set()
        self._max_depth = max_depth
        if with_call:
            self._options.add('call')
        if with_return:
            self._options.add('return')
        if with_exception:
            self._options.add('exception')

    def __call__(self, frame, event, arg):
        ret = []
        if event == 'call':
            back_frame = frame.f_back
            if back_frame in self._frame_dict:
                self._frame_dict[frame] = self._frame_dict[back_frame] + 1
            else:
                self._frame_dict[frame] = 0

        depth = self._frame_dict[frame]

        if event in self._options and (self._max_depth < 0 or depth <= self._max_depth):
            ret.append(frame.f_code.co_name)
            ret.append('[%s]' % event)
            if event == 'return':
                ret.append(arg)
            elif event == 'exception':
                ret.append(repr(arg[0]))
            ret.append('in %s line:%s' % (frame.f_code.co_filename, frame.f_lineno))
        if ret:
            print("%s%s" % ('  ' * depth, '\t'.join([str(i) for i in ret])))

        return self

    @staticmethod
    def stack_trace(**kw):
        def entangle(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                st = StackTrace(**kw)
                sys.settrace(st)
                try:
                    return func(*args, **kwargs)
                finally:
                    sys.settrace(None)
            return wrapper
        return entangle
