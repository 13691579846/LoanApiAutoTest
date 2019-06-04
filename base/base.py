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


class Base(unittest.TestCase):
    """用例入口"""
    @classmethod
    def setUpClass(cls):
        cls.mysql = HandleMysql()
        log.info('------开始执行{}测试用例------'.format(cls.__doc__))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        log.info('------{}测试用例执行结束------'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
