"""
------------------------------------
@Time : 2019/6/6 13:23
@Auth : linux超
@File : AddLoanApi.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from common.SendRequests import request
from common.ParseConfig import do_conf
from common.RecordLog import log


# 添加标的


class AddLoanApi(object):
    request = request  # 登录时的会话

    def add_loan_api(self, method, url, data):
        response = self.request(method=method,
                                url=url,
                                data=data
                                )
        return response

    def close(self):
        log.info('关闭添加标的请求...')
        self.request.close_session()


add = AddLoanApi()

if __name__ == '__main__':
    add = AddLoanApi()
    add.add_loan_api(method='post',
                     url=do_conf('URL', 'Host_Url') + '/member/login',
                     data={"mobilephone": "18987560249", "pwd": "123457"})
    add.request.close_session()
