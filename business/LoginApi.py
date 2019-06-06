"""
------------------------------------
@Time : 2019/6/1 14:21
@Auth : linux超
@File : test_Recharge_api.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
from common.SendRequests import request
from common.ParseConfig import do_conf
from common.RecordLog import log

# 登录


class LoginApi(object):
    request = request  # 登录时的会话

    def login_api(self, method, url, data):
        response = self.request(method=method,
                     url=url,
                     data=data
                     )
        log.info('投资人：{}登录接口'.format(data['mobilephone']))
        print(response.text)

    def close(self):
        log.info('关闭登录请求...')
        self.request.close_session()


login = LoginApi()

if __name__ == '__main__':
    login = LoginApi()
    login.login_api(method='post',
                    url=do_conf('URL', 'Host_Url')+'/member/login',
                    data={"mobilephone": "18987560249", "pwd": "123457"})
    login.request.close_session()
