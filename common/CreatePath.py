import os
from datetime import datetime, date

from config.config import PRO_DIR


class ModelsClass(object):
    def __init__(self):
        pass

    @staticmethod
    def get_current_date():
        """获取当前日期"""
        current_time = datetime.now().strftime(str(date.today()))
        return current_time

    @staticmethod
    def file_name(file_type):
        """日志与HTML报告文件名"""
        current_time = datetime.now().strftime(str(date.today()) + '-' + '%H-%M-%S')
        file_name = current_time + '.' + file_type
        return file_name

    @staticmethod
    def create_dir(path):
        """创建HTML报告与日志文件存放目录"""
        report_dir = os.path.join(PRO_DIR, path)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        return report_dir


if __name__ == '__main__':
    print(ModelsClass.create_dir('log'))
    print(ModelsClass.create_dir('report'))
    print(ModelsClass.file_name('html'))
    print(ModelsClass.get_current_date())
