"""
------------------------------------
@Time : 2019/6/1 18:24
@Auth : linux超
@File : RandomPhone.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
暂时没用, 考虑到如果单独使用这个类，需要再连接一次数据库，浪费资源
"""
import string
import random

from common.HandleMysql import HandleMysql


class PhoneNumber(object):
    def __init__(self):
        pass

    @staticmethod
    def phone_num():
        """随机生成3个角色的电话号码"""
        num_start = ['134', '135', '136', '137', '138',
                     '139', '150', '151', '152', '158',
                     '159', '157', '182', '187', '188',
                     '147', '130', '131', '132', '155',
                     '156', '185', '186', '133', '153',
                     '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits, 8))
        phone_number = start + end
        return phone_number

    @staticmethod
    def get_phone():
        """判断生成的电话号码是否存在数据库中"""
        db = HandleMysql()
        select_phone_sql = 'select MobilePhone from member;'
        phone_number = db(sql=select_phone_sql, is_all=True)
        db.close()
        phone_list = []
        for phone_dic in phone_number:  # [{'MobilePhone': '18825046772'}, {'MobilePhone': '18825046772'}]
            phone_list.append(list(phone_dic.values())[0])
        while 1:
            phone = PhoneNumber.phone_num()
            if phone not in phone_list:
                return phone
            print('函数内部的手机号', phone)

    @staticmethod
    def get_value_from_db():
        pass


if __name__ == '__main__':
    print(PhoneNumber.get_phone())
