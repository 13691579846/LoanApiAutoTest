"""
------------------------------------
@Time : 2019/5/20 9:37
@Auth : linux超
@File : RecordLog.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import logging
from logging import config

from config.config import LOG_PATH


class MyLog(object):

    def __init__(self):
        config.fileConfig(LOG_PATH)
        self.logger = logging.getLogger('example01')

    @property
    def my_logger(self):
        return self.logger


log = MyLog().my_logger


if __name__ == '__main__':
    log = MyLog()
    log.my_logger.info('it is my test log message info')
