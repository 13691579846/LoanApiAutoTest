"""
------------------------------------
@Time : 2019/6/1 14:20
@Auth : linux超
@File : test_Login_api.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest
import inspect
from openpyxl.styles.colors import RED, GREEN

from libs.ddt import (data, ddt)
from base.base import Base
from common.ParseExcel import do_excel
# from common.SendRequests import request
from common.DataReplace import do_replace
from common.HandleJson import HandleJson
from common.ParseConfig import do_conf
from common.RecordLog import log


@ddt
class TestLoginApi(Base):
    """登录接口"""
    test_data = do_excel.get_name_tuple_all_value(do_conf('SheetName', 'Login'))

    @data(*test_data)
    def test_login(self, value):
        row = value.CaseId + 1  # 用例ID所在行号
        title = value.Title  # 用例标题
        url = do_conf('URL', 'Host_Url') + value.URL  # 用例url
        request_value = value.Data  # 请求参数
        request_method = value.Method  # 请求方法
        log.info('开始执行登录-"{}"测试用例'.format(title))
        expected = HandleJson.json_to_python(value.Expected)  # 期望结果
        not_exist_phone = self.mysql.get_not_exist_phone()  # 逆向用例登录账号
        request_value = do_replace.register_login_parameters_data(not_exist_phone, request_value)
        response = self.request(request_method, url=url, data=request_value)
        actual_result = response.json()
        do_excel.write_cell(
            do_conf('SheetName', 'Login'),
            row,
            do_conf('ExcelNum', 'Actual_Column'),
            response.text)
        try:
            self.assertEqual(expected, actual_result, msg='测试{}失败'.format(title))
        except AssertionError as e:
            do_excel.write_cell(
                do_conf('SheetName', 'Login'),
                row,
                do_conf('ExcelNum', 'Result_Column'),
                do_conf('Result', 'Fail'),
                color=RED)
            log.error('{}-测试[{}] :Failed\nDetails:\n{}'.format(inspect.stack()[0][3], title, e))
            raise e
        else:
            do_excel.write_cell(
                do_conf('SheetName', 'Login'),
                row,
                do_conf('ExcelNum', 'Result_Column'),
                do_conf('Result', 'Pass'),
                color=GREEN)
            log.info('{}-测试[{}] :Passed'.format(inspect.stack()[0][3], title))
        log.info('执行登录-测试用例"{}"结束'.format(title))


if __name__ == '__main__':
    unittest.main()
