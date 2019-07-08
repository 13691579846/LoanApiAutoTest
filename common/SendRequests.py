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
        log.info('建立请求...')

    def send_request(self, method, url, params_type='form', data=None, **kwargs):
        method = method.upper()
        params_type = params_type.upper()
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                    data = eval(data)
        if 'GET' == method:
            response = self.session.request(method=method, url=url, params=data, **kwargs)
        elif 'POST' == method:
            if params_type == 'FORM':
                log.info("开始发送{}请求，URL为：{}，请求数据为:{}".format(method, url, data))
                response = self.session.request(method=method, url=url, data=data, **kwargs)
            elif params_type == 'JSON':
                response = self.session.request(method=method, url=url, json=data, **kwargs)
            else:
                response = self.session.request(method=method, url=url, **kwargs)
        else:
            log.error("请求方法错误：request method '{}' error ! please check".format(method))
            raise ValueError('request method "{}" error ! please check'.format(method))
        return response

    def __call__(self, method, url, params_type='form', data=None, **kwargs):
        return self.send_request(method, url,
                                 params_type=params_type,
                                 data=data,
                                 **kwargs)

    def close_session(self):
        self.session.close()
        try:
            log.info('关闭请求...')
            del self.session.cookies['JSESSIONID']
        except Exception:
            pass


request = HttpRequests()


if __name__ == '__main__':
    pass
