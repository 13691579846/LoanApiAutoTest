"""
------------------------------------
@Time : 2019/6/2 18:38
@Auth : linux超
@File : CreateUser.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from common.RecordLog import log
from common.HandleMysql import HandleMysql
from common.ParseConfig import do_conf
from common.SendRequests import HttpRequests
from config.config import USER_PATH


class CreateUser(object):

    def __init__(self):
        pass

    @staticmethod
    def register(reg_name='linux超', pwd='123456'):
        """注册帐号"""
        do_mysql = HandleMysql()
        request = HttpRequests()
        register_url = do_conf('URL', 'Host_Url') + '/member/register'
        while 1:
            phone = do_mysql.get_not_exist_phone()
            request_data = {"mobilephone": phone, "pwd": pwd, "regname": reg_name}
            request(method='post',
                    url=register_url,
                    data=request_data
                    )
            sql = 'select Id from member where MobilePhone=%s;'
            member = do_mysql(sql=sql, args=(phone,))
            if member:
                member_id = member['Id']
                break
        user_dic = {
            reg_name: {
                'MemberId': member_id,
                'MobilePhone': phone,
                'RegName': reg_name
            }
        }
        do_mysql.close()
        request.close_session()
        log.info('注册{}帐号成功\n帐号信息-userId{},userName{},mobilePhone{}'.
                 format(reg_name, member_id, reg_name, phone))
        return user_dic

    @staticmethod
    def create_uer_info():
        """创建3个角色的帐号"""
        user_dict = {}
        user_dict.update(CreateUser.register('Invest', '123456'))
        user_dict.update(CreateUser.register('Loan', '123457'))
        user_dict.update(CreateUser.register('Admin', '123458'))
        do_conf.write_config(user_dict, USER_PATH)
        return user_dict


register = CreateUser()


if __name__ == '__main__':
    user = CreateUser()
    invest = user.register(reg_name='投资人')['投资人']
    loan = user.register(reg_name='借款人')['借款人']
    admin = user.register(reg_name='管理员')['管理员']
    print(invest, loan, admin)
    print(user.create_uer_info())
