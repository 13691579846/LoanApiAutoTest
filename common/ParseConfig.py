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

from config.config import CONFIG_PATH, USER_PATH
from common.RecordLog import log


class ParseConfigFile(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        log.info('开始解析配置文件...')

    def get_option_value(self, section='DEFAULT', option=None, flag_eval=False, flag_bool=False):
        """获取配置文件指定section的option对应的value"""
        self.read(self.filename, encoding='utf-8')
        if option is None:
            return dict(self[section])
        if isinstance(flag_bool, bool):
            if flag_bool:
                return self.getboolean(section, option)
        else:
            raise ValueError('{} must be type bool'.format(flag_bool))
        data = self.get(section, option)
        if data.isdigit():
            data = int(data)
            log.info("从配置文件{}解析{}信息为{}".format(self.filename, option, data))
            return data
        try:
            data = float(data)
            log.info("从配置文件{}解析{}信息为{}".format(self.filename, option, data))
            return data
        except ValueError:
            pass
        if isinstance(flag_eval, bool):
            if flag_eval:
                data = eval(data)
                log.info("从配置文件{}解析{}信息为{}".format(self.filename, option, data))
                return data
        else:
            raise ValueError('{} must be type bool'.format(flag_eval))
        log.info("从配置文件{}解析{}信息为{}".format(self.filename, option, data))
        return data

    @classmethod
    def write_config(cls, data, path):
        """写配置文件"""
        conf_obj = cls(path)
        for value in data:
            conf_obj[value] = data[value]
            log.info('{}文件写入数据\n{}'.format(path, data))
        with open(path, 'w', encoding='utf-8') as f:
            conf_obj.write(f)

    def __call__(self, section='DEFAULT', option=None, flag_eval=False, flag_bool=False):
        return self.get_option_value(section=section, option=option, flag_eval=flag_eval, flag_bool=flag_bool)


do_conf = ParseConfigFile(CONFIG_PATH)
do_user = ParseConfigFile(USER_PATH)


if __name__ == '__main__':
    conf = ParseConfigFile(CONFIG_PATH)
    user_dic = {
        'user': {
            'memberId': 1,
            'mobile_phone': '12345678901',
            'reg_name': 'linux'
        }
    }
    conf.write_config(user_dic, r'D:\LeMonApiAutoTest\config\userinf.ini')
