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
import os

from common.HandleMysql import HandleMysql
from business.CreateUser import register
from common.RecordLog import log


class Base(unittest.TestCase):
    """用例入口"""

    phone_invest = register.register(reg_name='投资人')
    phone_loan = register.register(reg_name='借款人')
    phone_admin = register.register(reg_name='管理员')
    register.close()

    @classmethod
    def setUpClass(cls):
        cls.mysql = HandleMysql()
        log.info('开始执行{}测试用例'.format(cls.__doc__))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        log.info('{}测试用例执行结束'.format(cls.__doc__))


if __name__ == '__main__':
    unittest.main()
