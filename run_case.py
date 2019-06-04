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
from common.CreatePath import ModelsClass
from common.ParseConfig import do_conf
from config.config import ENVIRONMENT
from business.CreateUser import register
from config.config import USER_PATH


def create_user_info_config_file(filename):
    """创建3个角色用户配置文件"""
    if not os.path.exists(filename):
        register.create_uer_info()


def tc_suite():
    """测试套件"""
    discover = unittest.defaultTestLoader.discover('.', do_conf('FilePath', 'testcase'))
    return discover


if __name__ == '__main__':
    create_user_info_config_file(USER_PATH)
    report_dir = ModelsClass.create_dir(do_conf('FilePath', 'HtmlPathName'))
    report_file_name = ModelsClass.file_name('html')
    with open(report_dir + '/' + report_file_name, 'wb') as f:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=f,
                                                  description=ENVIRONMENT,
                                                  title='前程贷项目接口自动化测试报告',
                                                  tester='linux超',
                                                  verbosity=2)
        runner.run(tc_suite())
