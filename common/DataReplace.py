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


class DataReplace(object):
    def __init__(self):
        pass

    @staticmethod
    def re_replace(re_expression, data, source):
        """
        替换指定字符串
        :param re_expression: 正则表达式
        :param data: 替换字符串
        :param source: 目标替换源字符串
        :return:
        """
        if isinstance(data, str):
            pattern = re.compile(re_expression)
            if re.search(pattern, source):
                source = re.sub(pattern, data, source)
            return source
        else:
            raise TypeError("data '{}' must be string".format(data))

    def __call__(self, re_expression, data, source):
        return self.re_replace(re_expression, data, source)


do_replace = DataReplace()


if __name__ == '__main__':
    source_str_phone = '{"mobilephone": ${MobilePhone}, "pwd": "123456"}'
    source_str_pwd = '{"mobilephone": ${MobilePhone}, "pwd": "${pwd}"}'
    source_str = '{"mobilephone": "13691579846", "pwd": "${pwd}"}'
    expression_phone = r'\$\{MobilePhone\}'
    expression_pwd = r'\$\{pwd\}'
    phone = '13691579846'
    pwd = '123456'
    data_replace = DataReplace()
    print(data_replace(expression_phone, phone, source_str_phone))
    print(data_replace(expression_pwd, pwd, source_str_pwd))
    print(data_replace(expression_pwd, pwd, source_str))
