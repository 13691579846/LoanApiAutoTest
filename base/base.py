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


class Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()


if __name__ == '__main__':
    unittest.main()
