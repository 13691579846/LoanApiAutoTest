import os
import platform

from common.CreatePath import ModelsClass

"""
This module stores the file directories and files needed by the project
"""
"""
All dirs of the project
"""
PRO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CASE_DIR = os.path.join(PRO_DIR, 'cases')
DATA_DIR = os.path.join(PRO_DIR, 'data')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.ini')
DATA_PATH = os.path.join(DATA_DIR, 'testcases.xlsx')
USER_PATH = os.path.join(CONFIG_DIR, 'userinfo.ini')
"""
log & Report name and dir
"""
LOG_NAME = ModelsClass.file_name('log')
LOG_DIR = os.path.join(PRO_DIR, 'log')#ModelsClass.create_dir('log')
CREATE_LOG_DIR = ModelsClass.create_dir(LOG_DIR)
LOG_PATH = os.path.join(LOG_DIR, LOG_NAME)
REPORT_DIR = os.path.join(PRO_DIR, 'report')
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


if __name__ == '__main__':
    print('项目目录', PRO_DIR)
    print('配置文件目录', CONFIG_DIR)
    print('用例目录', CASE_DIR)
    print('测试数据目录', DATA_DIR)
    print('配置文件路径', CONFIG_PATH)
    print('日志配置文件路径', LOG_PATH)
    print('测试数据文件路径', DATA_PATH)
    print('账户信息文件路径', USER_PATH)
    print(LOG_NAME)
