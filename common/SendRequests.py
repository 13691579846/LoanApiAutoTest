"""
------------------------------------
@Time : 2019/5/28 9:10
@Auth : linux超
@File : SendRequests.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import json
import requests

from common.RecordLog import log


class HttpRequests(object):
    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method, url,
                     params_type='form', data=None,
                     headers=None, files=None, **kwargs):
        method = method.upper()
        params_type = params_type.upper()
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                try:
                    data = eval(data)
                except Exception as e:
                    raise e
        if 'GET' == method:
            response = self.session.request(method=method, url=url, params=data, headers=headers, **kwargs)
        elif 'POST' == method:
            if params_type == 'FORM':
                log.info("开始发送{}请求，URL为：{}，请求数据为:{}".format(method, url, data))
                response = self.session.request(method=method, url=url, data=data, headers=headers,
                                                files=files, **kwargs)
            elif params_type == 'JSON':
                response = self.session.request(method=method, url=url, json=data, headers=headers,
                                                files=files, **kwargs)
            else:
                log.error("请求数据格式错误：request params type '{}' error ! please check".format(params_type))
                raise ValueError('request params type "{}" error ! please check'.format(params_type))
        else:
            log.error("请求方法错误：request method '{}' error ! please check".format(method))
            raise ValueError('request method "{}" error ! please check'.format(method))
        return response

    def __call__(self, method, url, params_type='form', data=None, headers=None, cookies=None, files=None, **kwargs):
        return self.send_request(method, url,
                                 params_type=params_type,
                                 data=data,
                                 headers=headers, files=files, **kwargs)

    def close_session(self):
        self.session.close()
        try:
            del self.session.cookies['JSESSIONID']
        except Exception:
            pass


request = HttpRequests()


if __name__ == '__main__':
    request = HttpRequests()
    request2 = HttpRequests()
    login_url = r'http://test.lemonban.com:8080/futureloan/mvc/api/member/login'
    login_data = {"mobilephone": "13691579822", "pwd": "123456"}
    recharge_url = r'http://test.lemonban.com:8080/futureloan/mvc/api/member/recharge'
    recharge_data = {"mobilephone": "13691579822", "amount": 10000}
    login = request('post', url=login_url, data=login_data)
    print(login.json())
    recharge = request('post', url=recharge_url, data=recharge_data)
    print(recharge.json())
    request.close_session()
    recharge = request('post', url=recharge_url, data=recharge_data)
    print(recharge.json())
