"""
------------------------------------
@Time : 2019/5/18 18:12
@Auth : linux超
@File : RecordLog.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import logging
from logging.handlers import RotatingFileHandler

from config.config import LOG_PATH


class Log(object):
    def __init__(self, name=__name__, path='mylog.log', level='DEBUG'):
        self.__name = name
        self.__path = path
        self.__level = level
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level)

    def __ini_handler(self):
        """初始化handler"""
        stream_handler = logging.StreamHandler()
        # file_handler = logging.FileHandler(self.__path, encoding='utf-8')
        file_handler = RotatingFileHandler(self.__path, maxBytes=10*1024*1024, backupCount=3, encoding = 'utf-8')
        return stream_handler, file_handler

    def __set_handler(self, stream_handler, file_handler, level='DEBUG'):
        """设置handler级别并添加到logger收集器"""
        stream_handler.setLevel(level)
        file_handler.setLevel(level)
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def __set_formatter(self, stream_handler, file_handler):
        """设置日志输出格式"""
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s-[日志信息]: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    def __close_handler(self, stream_handler, file_handler):
        """关闭handler"""
        stream_handler.close()
        file_handler.close()

    @property
    def Logger(self):
        """构造收集器，返回looger"""
        stream_handler, file_handler = self.__ini_handler()
        self.__set_handler(stream_handler, file_handler)
        self.__set_formatter(stream_handler, file_handler)
        self.__close_handler(stream_handler, file_handler)
        return self.__logger


log = Log(__name__, LOG_PATH).Logger


if __name__ == '__main__':
    log = Log(__name__, 'file.log')
    logger = log.Logger
    logger.debug('I am a debug message')
    logger.info('I am a info message')
    logger.warning('I am a warning message')
    logger.error('I am a error message')
    logger.critical('I am a critical message')
