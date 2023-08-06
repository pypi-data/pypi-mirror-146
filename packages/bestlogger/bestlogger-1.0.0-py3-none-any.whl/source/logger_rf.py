from robot.api import logger


class RobotLogger:
    def __init__(self):
        try:
            self.EXECUTION_CONTEXTS = logger.EXECUTION_CONTEXTS
        except Exception as e:
            print(e)
            self.EXECUTION_CONTEXTS = logger.get_execution_contexts()

    @staticmethod
    def write(msg, level='INFO', html=False):
        """Writes the message to the log file using the given level.

        Valid log levels are ``TRACE``, ``DEBUG``, ``INFO`` (default since RF
        2.9.1), ``WARN``, and ``ERROR`` (new in RF 2.9). Additionally it is
        possible to use ``HTML`` pseudo log level that logs the message as HTML
        using the ``INFO`` level.

        Instead of using this method, it is generally better to use the level
        specific methods such as ``info`` and ``debug`` that have separate
        ``html`` argument to control the message format.
        """
        logger.write(msg, level, html)

    def trace(self, msg, html=False):
        """Writes the message to the log file using the ``TRACE`` level."""
        self.write(msg, 'TRACE', html)

    def debug(self, msg, html=False):
        """Writes the message to the log file using the ``DEBUG`` level."""
        self.write(msg, 'DEBUG', html)

    def info(self, msg, html=False, also_console=False):
        """Writes the message to the log file using the ``INFO`` level.

        If ``also_console`` argument is set to ``True``, the message is
        written both to the log file and to the console.
        """
        self.write(msg, 'INFO', html)
        if also_console:
            self.console(msg)

    def warn(self, msg, html=False):
        """Writes the message to the log file using the ``WARN`` level."""
        self.write(msg, 'WARN', html)

    def warning(self, msg, html=False):
        """Writes the message to the log file using the ``WARN`` level."""
        self.write(msg, 'WARN', html)

    def critical(self, msg, html=False):
        self.write(msg, 'INFO', html)

    def error(self, msg, html=False):
        """Writes the message to the log file using the ``ERROR`` level.

        New in Robot Framework 2.9.
        """
        self.write(msg, 'ERROR', html)

    @staticmethod
    def console(msg, newline=True, stream='stdout'):
        """Writes the message to the console.

        If the ``newline`` argument is ``True``, a newline character is
        automatically added to the message.

        By default the message is written to the standard output stream.
        Using the standard error stream is possibly by giving the ``stream``
        argument value ``'stderr'``.
        """
        logger.console(msg, newline, stream)
