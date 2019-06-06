"""
------------------------------------
@Time : 2019/6/1 14:26
@Auth : linux超
@File : run_case.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import os
import unittest

from libs import HTMLTestRunnerNew
from config.config import (ENVIRONMENT, USER_PATH, REPORT_DIR, CASE_DIR)
from business.CreateUser import register
from common.ParseConfig import do_conf
from common.CreatePath import ModelsClass


def create_user_info_config_file(filename):
    """创建3个角色用户配置文件"""
    if not os.path.exists(filename):
        register.create_uer_info()


def tc_suite():
    """测试套件"""
    discover = unittest.defaultTestLoader.discover(CASE_DIR, 'test_*.py')
    return discover


if __name__ == '__main__':
    create_user_info_config_file(USER_PATH)
    report_dir = ModelsClass.create_dir(REPORT_DIR)
    report_file_name = ModelsClass.file_name('html')
    with open(report_dir + '/' + report_file_name, 'wb') as f:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=f,
                                                  description=ENVIRONMENT,
                                                  title=do_conf('Project', 'PRO_NAME'),
                                                  tester=do_conf('Project', 'Tester'),
                                                  verbosity=2)
        runner.run(tc_suite())
