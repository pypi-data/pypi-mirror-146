import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
SEQ_DICT = {
    "$RESET": "\033[0m",
    "$GREEN": "\033[0;36m",
    "$YELLOW": "\033[0;32m",
}
COLOR_SEQ = "\033[1;%dm"
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': RED + 10,
    'ERROR': RED
}


def formatter_message(message, use_color=True):
    if use_color:
        for seq, col in SEQ_DICT.items():
            message = message.replace(seq, col)
    else:
        for seq, col in SEQ_DICT.items():
            message = message.replace(seq, '')
    return message


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        message = record.msg
        if type(message) != dict and type(message) != list:
            if type(message) != str:
                try:
                    message = str(message)
                except Exception as e:
                    print(e)
            if self.use_color and levelname in COLORS and type(message) == str:
                levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + SEQ_DICT['$RESET']
                record.levelname = levelname_color
                record.msg = COLOR_SEQ % (30 + COLORS[levelname]) + message + SEQ_DICT['$RESET']
        return logging.Formatter.format(self, record)
