"""
------------------------------------
@Time : 2019/6/1 14:26
@Auth : linux超
@File : run_case.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest

from libs import HTMLTestRunnerNew
from common.CreatePath import ModelsClass
from common.ParseConfig import do_conf
from config.config import ENVIRONMENT


def tc_suite():
    discover = unittest.defaultTestLoader.discover('.', do_conf('FilePath', 'testcase'))
    return discover


if __name__ == '__main__':
    report_dir = ModelsClass.create_dir(do_conf('FilePath', 'HtmlPathName'))
    report_file_name = ModelsClass.file_name('html')
    log_file_dir = ModelsClass.create_dir(do_conf('FilePath', 'LogPathName'))
    with open(report_dir + '/' + report_file_name, 'wb') as f:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=f,
                                                  description=ENVIRONMENT,
                                                  title='前程贷项目接口自动化测试报告',
                                                  tester='linux超',
                                                  verbosity=2)
        runner.run(tc_suite())
