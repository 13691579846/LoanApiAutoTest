import os
import platform

from common.CreatePath import ModelsClass

"""
create log dir
"""
LOG_DIR = ModelsClass.create_dir('log')
"""
This module stores the file directories and files needed by the project
"""
PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CASE_DIR = os.path.join(PRO_DIR, 'cases')
DATA_DIR = os.path.join(PRO_DIR, 'data')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.ini')
DATA_PATH = os.path.join(DATA_DIR, 'testcases.xlsx')
LOG_PATH = os.path.join(LOG_DIR, 'test_log.log')
USER_PATH = os.path.join(DATA_DIR, 'userinfo.txt')
"""
Test environment info
"""
ENVIRONMENT = \
    "Windows Version:" + \
    platform.system() + \
    platform.version() + \
    platform.release() + \
    "Python Version" + \
    platform.python_build()[0]
"""
request base url
"""
BASE_URL = r'http://test.lemonban.com:8080/futureloan/mvc/api'


if __name__ == '__main__':
    print('项目目录', PRO_DIR)
    print('配置文件目录', CONFIG_DIR)
    print('用例目录', CASE_DIR)
    print('测试数据目录', DATA_DIR)
    print('配置文件路径', CONFIG_PATH)
    print('日志配置文件路径', LOG_PATH)
    print('测试数据文件路径', DATA_PATH)
    print('账户信息文件路径', USER_PATH)
