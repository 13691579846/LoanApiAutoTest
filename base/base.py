"""
------------------------------------
@Time : 2019/6/1 22:13
@Auth : linux超
@File : base.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest

from common.HandleMysql import HandleMysql
from common.RecordLog import log
from common.SendRequests import HttpRequests


class Base(unittest.TestCase):
    """用例入口"""
    mysql = HandleMysql()
    @classmethod
    def setUpClass(cls):
        cls.request = HttpRequests()
        cls.mysql = HandleMysql()
        log.info('------开始执行{}测试用例------'.format(cls.__doc__))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        cls.request.close_session()
        log.info('------{}测试用例执行结束------'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
