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
    # add by linux超 at 2019.06.06
    pattern_exist_loan_member_id = re.compile(do_conf('Expression', 'Existed_member_id'))
    pattern_not_exist_loan_member_id = re.compile(do_conf('Expression', 'Non_existed_member_id'))
    # add by linux超 at 2019.06.06
    pattern_exist_invest_member_id = re.compile(do_conf('Expression', 'Exist_invest_member_id'))
    pattern_not_exist_invest_member_id = re.compile(do_conf('Expression', 'Non_exist_invest_member_id'))
    pattern_exist_loan_id = re.compile(do_conf('Expression', 'Exist_loan_id'))
    pattern_not_exist_loan_id = re.compile(do_conf('Expression', 'Non_exist_loan_id'))
    pattern_amount = re.compile(do_conf('Expression', 'Amount'))
    pattern_password = re.compile(do_conf('Expression', 'Password'))
    pattern_amount_not_enough = re.compile(do_conf('Expression', 'Amount_not_enough'))  # 标的金额不足
    pattern_amount_remain_amount = re.compile(do_conf('Expression', 'Remain_amount'))  # 标的剩余金额(用来测试满标)

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

    # --------注册与登录接口参数化--------
    @classmethod
    def replace_not_exist_phone(cls, not_exist_phone, data):
        """替换未注册的手机号"""
        data = cls.re_replace(cls.pattern_not_exist_phone, not_exist_phone, data)
        return data

    @classmethod
    def replace_exist_phone(cls, data):
        """替换已经注册的手机号码"""
        exist_phone = str(do_user('Invest', 'MobilePhone'))
        data = cls.re_replace(cls.pattern_exist_phone, exist_phone, data)
        return data

    # -----------充值接口参数化-----------
    @classmethod
    def replace_invest_phone(cls, data):
        """充值接口替换登录的角色帐号"""
        login_phone = str(do_user('Loan', 'MobilePhone'))
        data = cls.re_replace(cls.pattern_invest_phone, login_phone, data)
        return data

    @classmethod
    def replace_no_login_phone(cls, data):
        """充值接口替换未登录的角色帐号"""
        no_login_phone = str(do_user('Loan', 'MobilePhone'))
        data = cls.re_replace(cls.pattern_no_login_phone, no_login_phone, data)
        return data

    # ----------加标接口参数化-------------
    # add by linux超 at 2019.06.06
    @classmethod
    def replace_loan_member_id(cls, data):
        """替换借款人的member id"""
        loan_member_id = str(do_user('Loan', 'memberid'))
        data = cls.re_replace(cls.pattern_exist_loan_member_id, loan_member_id, data)
        return data

    # add by linux超 at 2019.06.06
    @classmethod
    def replace_no_exist_loan_member_id(cls, not_exist_loan_member_id, data):
        """替换不存在的loan member id"""
        data = cls.re_replace(cls.pattern_not_exist_loan_member_id, not_exist_loan_member_id, data)
        return data

    # -----------竞标接口参数化-----------
    @classmethod
    def replace_exist_invest_id(cls, data):
        invest_member_id = str(do_user('Invest', 'memberid'))
        data = cls.re_replace(cls.pattern_exist_invest_member_id, invest_member_id, data)
        return data

    @classmethod
    def replace_exist_loan_id(cls, data):
        exist_loan_id = getattr(DataReplace, 'loan_id')
        data = cls.re_replace(cls.pattern_exist_loan_id, exist_loan_id, data)
        return data

    @classmethod
    def replace_not_exist_invest_id(cls, data):
        if hasattr(DataReplace, 'non_exist_member_id'):
            not_exist_invest_id = getattr(DataReplace, 'non_exist_member_id')
            data = cls.re_replace(cls.pattern_not_exist_invest_member_id, not_exist_invest_id, data)
        else:
            data = cls.re_replace(cls.pattern_not_exist_invest_member_id, '', data)
        return data

    @classmethod
    def replace_not_exist_loan_id(cls, data):
        if hasattr(DataReplace, 'non_exist_loan_id'):
            not_exist_loan_id = getattr(DataReplace, 'non_exist_loan_id')
            data = cls.re_replace(cls.pattern_not_exist_loan_id, not_exist_loan_id, data)
        else:
            data = cls.re_replace(cls.pattern_not_exist_loan_id, '', data)
        return data

    @classmethod
    def replace_password(cls, data):
        pwd = str(do_user('Invest', 'pwd'))
        data = cls.re_replace(cls.pattern_password, pwd, data)
        return data

    @classmethod
    def replace_amount(cls, data):
        amount = '2000'
        data = cls.re_replace(cls.pattern_amount, amount, data)
        return data

    @classmethod
    def replace_amount_not_enough(cls, data):
        amount = str(do_conf('add_loan_api', 'amount'))
        data = cls.re_replace(cls.pattern_amount_not_enough, amount, data)
        return data

    @classmethod
    def replace_remain_amount(cls, data):
        if hasattr(DataReplace, 'remain_amount'):
            # 总金额-已投金额 = 需要满标时的投资金额
            amount = str(float(do_conf('add_loan_api', 'amount')) - getattr(DataReplace, 'remain_amount'))
            data = cls.re_replace(cls.pattern_amount_remain_amount, amount, data)
        else:
            data = cls.re_replace(cls.pattern_amount_remain_amount, '', data)
        return data

    @classmethod
    def register_login_parameters_data(cls, not_exist_phone, data):
        """注册与登录参数化"""
        data = cls.replace_not_exist_phone(not_exist_phone, data)
        data = cls.replace_exist_phone(data)
        return data

    @classmethod
    def recharge_parameters_data(cls, data):
        """充值的参数化"""
        data = cls.replace_invest_phone(data)
        data = cls.replace_no_login_phone(data)
        return data

    # add by linux超 at 2019.06.06
    @classmethod
    def add_parameters_data(cls, not_exist_loan_member_id, data):
        """加标的参数化"""
        data = cls.replace_loan_member_id(data)
        data = cls.replace_no_exist_loan_member_id(not_exist_loan_member_id, data)
        return data

    @classmethod
    def invest_parameters_data(cls, data):
        """竞标接口的参数化（投资人已经登录标的存在且为竞标状态）"""
        data = cls.replace_exist_invest_id(data)
        data = cls.replace_exist_loan_id(data)
        data = cls.replace_not_exist_invest_id(data)
        data = cls.replace_password(data)
        data = cls.replace_amount(data)
        data = cls.replace_not_exist_loan_id(data)
        data = cls.replace_amount_not_enough(data)
        data = cls.replace_remain_amount(data)
        return data


register_login_parameters = getattr(DataReplace, 'register_login_parameters_data')
recharge_parameters = getattr(DataReplace, 'recharge_parameters_data')
add_parameters = getattr(DataReplace, 'add_parameters_data')
invest_parameters = getattr(DataReplace, 'invest_parameters_data')

if __name__ == '__main__':
    source_str_phone = '{"mobilephone": ${not_exist_phone}, "pwd": "123456"}'
    data_phone = '{"mobilephone": ${exist_phone}, "pwd": "123456"}'
    invest_phone = '{"mobilephone": ${Invest}, "pwd": "123456"}'
    print(DataReplace.register_login_parameters_data('1391111111', invest_phone))
    setattr(DataReplace, 'loan_id', '123456')
    setattr(DataReplace, 'non_exist_member_id', '654321')
    setattr(DataReplace, 'not_exist_loan_id', '242434')
    value = '{"memberId":"${invest_memberID}", "pwd": [123456], "loanId": "${loanID}","amount":"${amount}"}'
    new_value = DataReplace.invest_parameters_data(value)
    print(new_value)
