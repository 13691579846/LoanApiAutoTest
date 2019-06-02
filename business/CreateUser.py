"""
------------------------------------
@Time : 2019/6/2 18:38
@Auth : linux超
@File : CreateUser.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from common.HandleMysql import HandleMysql
from common.ParseConfig import do_conf
from common.DataReplace import do_replace
from common.SendRequests import request


class CreateUser(object):
    def __init__(self):
        self.do_mysql = HandleMysql()

    def register(self, reg_name='linux超'):
        """
        注册接口
        :param reg_name:
        :param request_method: post or get
        :param url:
        :param request_value: '{"mobilephone": "${MobilePhone}", "pwd": "123456", "regname": "${RegName}"}'
        :return: Pass
        """
        phone_dic = {reg_name: None}
        expression_phone = do_conf('Expression', 'phone_number')
        expression_name = r'\$\{RegName\}'
        phone = self.do_mysql.get_phone()
        request_value = do_replace(expression_phone, phone, do_conf('register', 'request_data'))
        request_value = do_replace(expression_name, reg_name, request_value)
        request(do_conf('register', 'request_method'), url=do_conf('register', 'register_url'), data=request_value)
        phone_dic[reg_name] = phone
        return phone_dic

    def is_user_file_exist(self):
        import os
        from config.config import USER_PATH
        if os.path.isfile(USER_PATH):
            with open(USER_PATH, encoding='utf-8') as f:
                for line in f:
                    print(line)
        else:
            with open(USER_PATH, 'w', encoding='utf-8') as f:
                phone_invest = self.register(reg_name='投资人')['投资人']
                f.write('投资人:{}\n'.format(phone_invest))
                phone_loan = self.register(reg_name='借款人')['借款人']
                f.write('借款人:{}\n'.format(phone_loan))
                phone_admin = self.register(reg_name='管理员')['管理员']
                f.write('管理人:{}\n'.format(phone_admin))
                self.do_mysql.close()

    def close(self):
        self.do_mysql.close()


register = CreateUser()


if __name__ == '__main__':
    user = CreateUser()
    # phone_invest = user.register(reg_name='投资人')['投资人']
    # phone_loan = user.register(reg_name='借款人')['借款人']
    # phone_admin = user.register(reg_name='管理员')['管理员']
    # print(phone_invest, phone_loan, phone_admin)
    # user.close()
    user.is_user_file_exist()
