"""
------------------------------------
@Time : 2019/5/16 9:11
@Auth : linux超
@File : ParseConfig.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from configparser import ConfigParser

from config.config import CONFIG_PATH


class ParseConfigFile(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        try:
            self.filename = filename
            self.read(filename, encoding='utf-8')
        except Exception as e:
            raise e

    def get_option_value(self, section='DEFAULT', option=None, flag_eval=False, flag_bool=False):
        if option is None:
            return dict(self[section])
        if isinstance(flag_bool, bool):
            if flag_bool:
                return self.getboolean(section, option)
        else:
            raise ValueError('{} must be type bool'.format(flag_bool))
        data = self.get(section, option)
        if data.isdigit():
            return int(data)
        try:
            return float(data)
        except ValueError:
            pass
        if isinstance(flag_eval, bool):
            if flag_eval:
                return eval(data)
        else:
            raise ValueError('{} must be type bool'.format(flag_eval))
        return data

    def __call__(self, section='DEFAULT', option=None, flag_eval=False, flag_bool=False):
        return self.get_option_value(section=section, option=option, flag_eval=flag_eval, flag_bool=flag_bool)


do_conf = ParseConfigFile(CONFIG_PATH)


if __name__ == '__main__':
    conf = ParseConfigFile(CONFIG_PATH)
    print(conf('FilePath', 'TestCase'))
    print(conf('FilePath', 'LogPath'))
    print(conf('ExcelNum', 'actual_column_num'))
    print(conf('ExcelNum', 'result_column_num'))
    print(conf('Result', 'result_pass'))
