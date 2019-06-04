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
from common.SendRequests import HttpRequests
from config.config import USER_PATH
# from common.HandleJson import HandleJson


class CreateUser(object):

    def __init__(self):
        pass

    @staticmethod
    def register(reg_name='linux超', pwd='123456'):
        request = HttpRequests()
        do_mysql = HandleMysql()
        # phone_dic = {reg_name: None}
        request_value = do_conf('register', 'request_value')
        expression_phone = do_conf('Expression', 'phone_number')
        expression_name = do_conf('Expression', 'reg_name')
        expression_pwd = do_conf('Expression', 'pwd')
        phone = do_mysql.get_phone()
        request_value = do_replace(expression_phone, phone, request_value)
        request_value = do_replace(expression_name, reg_name, request_value)
        request_value = do_replace(expression_pwd, pwd, request_value)
        request(do_conf('register', 'request_method'), url=do_conf('register', 'register_url'), data=request_value)
        sql = "select Id from member where MobilePhone=%s"
        result = do_mysql(sql=sql, args=(phone, ))
        if result:
            user_id = result['Id']
            user_dic = {
                    'regname': reg_name,
                    'id': user_id,
                    'phone': phone
            }
            # phone_dic[reg_name] = phone
            do_mysql.close()
            request.close_session()
            return user_dic

    @staticmethod
    def uer_info(path):
        import os
        if not os.path.exists(path):
            phone_invest = CreateUser.register('投资人')
            phone_loan = CreateUser.register('借款人')
            phone_admin = CreateUser.register('管理人')

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
    invest = user.register(reg_name='投资人')['投资人']
    loan = user.register(reg_name='借款人')['借款人']
    admin = user.register(reg_name='管理员')['管理员']
    print(invest, loan, admin)
    print(user.uer_info(USER_PATH))
