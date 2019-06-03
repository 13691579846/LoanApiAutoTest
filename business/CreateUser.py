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
from config.config import USER_PATH


class CreateUser(object):
    def __init__(self):
        # self.do_mysql = HandleMysql()
        pass

    @staticmethod
    def register(reg_name='linux超'):
        do_mysql = HandleMysql()
        phone_dic = {reg_name: None}
        expression_phone = do_conf('Expression', 'phone_number')
        expression_name = r'\$\{RegName\}'
        phone = do_mysql.get_phone()
        request_value = do_replace(expression_phone, phone, do_conf('register', 'request_data'))
        request_value = do_replace(expression_name, reg_name, request_value)
        request(do_conf('register', 'request_method'), url=do_conf('register', 'register_url'), data=request_value)
        phone_dic[reg_name] = phone
        do_mysql.close()
        return phone_dic

    @staticmethod
    def uer_info(path):
        import os
        if not os.path.exists(path):
            phone_invest = CreateUser.register('投资人')['投资人']
            phone_loan = CreateUser.register('借款人')['借款人']
            phone_admin = CreateUser.register('管理人')['管理人']
            with open(USER_PATH, 'w', encoding='utf-8') as f:
                f.write('投资人:'+phone_invest+'\n'+'借款人:'+phone_loan+'\n'+'管理人:'+phone_admin)
        phone_list = []
        with open(path, encoding='utf-8') as f:
            for line in f:
                phone_list.append(tuple(line.strip().split(':')))
        return dict(phone_list)


register = CreateUser()


if __name__ == '__main__':
    user = CreateUser()
    # phone_invest = user.register(reg_name='投资人')['投资人']
    # phone_loan = user.register(reg_name='借款人')['借款人']
    # phone_admin = user.register(reg_name='管理员')['管理员']
    # print(phone_invest, phone_loan, phone_admin)
    print(user.uer_info(USER_PATH))

