"""
------------------------------------
@Time : 2019/6/2 18:38
@Auth : linux超
@File : register.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from common.HandleMysql import HandleMysql


def register(cls, request_method='post',
             url=r'http://test.lemonban.com:8080/futureloan/mvc/api//member/register',
             request_value='{"mobilephone": "${MobilePhone}", "pwd": "123456", "regname": "${RegName}"}',
             regname='linux超'):
    """
    注册接口
    :param regname:
    :param request_method: post or get
    :param url:
    :param request_value: '{"mobilephone": "${MobilePhone}", "pwd": "123456", "regname": "${RegName}"}'
    :return: Pass
    """
    phone_dic = {regname: None}
    expression_phone = do_conf('Expression', 'phone_number')
    expression_name = r'\$\{RegName\}'
    phone = cls.mysql.get_phone()
    request_value = do_replace(expression_phone, phone, request_value)
    request_value = do_replace(expression_name, regname, request_value)
    request(request_method, url=url, data=request_value)
    phone_dic[regname] = phone
    return phone_dic