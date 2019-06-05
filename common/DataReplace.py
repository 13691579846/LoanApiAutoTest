"""
------------------------------------
@Time : 2019/6/1 19:25
@Auth : linux超
@File : DataReplace.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import re

from common.RecordLog import log
from common.ParseConfig import (do_conf, do_user)


class DataReplace(object):

    pattern_not_exist_phone = re.compile(do_conf('Expression', 'Non_exist_phone'))
    pattern_exist_phone = re.compile(do_conf('Expression', 'Existed_phone'))
    pattern_invest_phone = re.compile(do_conf('Expression', 'Invest_phone'))
    pattern_no_login_phone = re.compile(do_conf('Expression', 'NoLogin_phone'))

    def __init__(self):
        pass

    @staticmethod
    def re_replace(re_expression, data, source):
        """
        替换指定字符串
        :param re_expression: 正则表达式
        :param data: 被替换字符串如手机号，密码等
        :param source: 目标源字符串
        :return:
        """
        if isinstance(data, str):
            pattern = re.compile(re_expression)
            if re.search(pattern, source):
                source = re.sub(pattern, data, source)
            log.info("测试数据{}通过正则匹配为: {}".format(source, source))
            return source
        else:
            log.error("正则匹配测试数据失败: data '{}' must be string".format(data))
            raise TypeError("data '{}' must be string".format(data))

    def replace_not_exist_phone(self, not_exist_phone, data):
        """替换未注册的手机号"""
        data = self.re_replace(self.pattern_not_exist_phone, not_exist_phone, data)
        return data

    def replace_exist_phone(self, data):
        """替换已经注册的手机号码"""
        exist_phone = str(do_user('Invest', 'MobilePhone'))
        data = self.re_replace(self.pattern_exist_phone, exist_phone, data)
        return data

    def replace_invest_phone(self, data):
        """充值接口替换登录的角色帐号"""
        login_phone = str(do_user('Loan', 'MobilePhone'))
        data = self.re_replace(self.pattern_invest_phone, login_phone, data)
        return data

    def replace_no_login_phone(self, data):
        """充值接口替换未登录的角色帐号"""
        no_login_phone = str(do_user('Loan', 'MobilePhone'))
        data = self.re_replace(self.pattern_no_login_phone, no_login_phone, data)
        return data

    def register_login_parameters_data(self, not_exist_phone, data):
        """注册与登录参数化"""
        data = self.replace_not_exist_phone(not_exist_phone, data)
        data = self.replace_exist_phone(data)
        return data

    def recharge_parameters_data(self, data):
        """充值的参数化"""
        data = self.replace_invest_phone(data)
        data = self.replace_no_login_phone(data)
        return data


do_replace = DataReplace()
# 注册参数化
register_login_parameters = getattr(do_replace, 'register_login_parameters_data')
recharge_parameters = getattr(do_replace, 'recharge_parameters_data')

if __name__ == '__main__':
    source_str_phone = '{"mobilephone": ${not_exist_phone}, "pwd": "123456"}'
    data_phone = '{"mobilephone": ${exist_phone}, "pwd": "123456"}'
    invest_phone = '{"mobilephone": ${Invest}, "pwd": "123456"}'
    data_replace = DataReplace()
    print(data_replace.register_login_parameters_data('1391111111', invest_phone))
