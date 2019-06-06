"""
------------------------------------
@Time : 2019/6/6 13:35
@Auth : linux超
@File : AuditApi.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from common.SendRequests import request
from common.ParseConfig import do_conf
from common.RecordLog import log


# 审核标的


class AuditLoanApi(object):
    request = request  # 登录时的会话

    def audit_loan_api(self, method, url, data):
        response = self.request(method=method,
                     url=url,
                     data=data
                     )
        print(response.text)

    def close(self):
        log.info('关闭添加标的请求...')
        self.request.close_session()


audit = AuditLoanApi()

if __name__ == '__main__':
    audit = AuditLoanApi()
    audit.audit_loan_api(method='post',
                         url=do_conf('URL', 'Host_Url') + '/member/login',
                         data={"mobilephone": "18987560249", "pwd": "123457"})
    audit.request.close_session()
