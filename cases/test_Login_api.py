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
import sys
from openpyxl.styles.colors import RED, GREEN

from config.config import BASE_URL
from libs.ddt import (data, ddt)
from base.base import Base
from common.ParseExcel import do_excel
from common.SendRequests import request
from common.DataReplace import do_replace
from common.HandleJson import HandleJson
from common.ParseConfig import do_conf
from common.RecordLog import log


@ddt
class TestLoginApi(Base):
    """登录接口"""
    test_data = do_excel.get_name_tuple_all_value(do_conf('SheetName', 'sheet_login'))

    @data(*test_data)
    def test_login(self, value):
        row = value.CaseId + 1  # 用例ID所在行号
        precondition = value.Precondition  # 前置条件
        title = value.Title  # 用例标题
        url = BASE_URL + value.URL  # 用例url
        request_value = value.Data  # 请求参数
        request_method = value.Method  # 请求方法
        log.info('开始执行登录-"{}"测试用例'.format(title))
        expected = HandleJson.json_to_python(value.Expected)  # 期望结果
        expression_phone = do_conf('Expression', 'phone_number')  # 正则表达式
        if precondition == '手机号未注册':
            phone = self.mysql.get_phone()
            request_value = do_replace(expression_phone, phone, request_value)
        else:
            request_value = do_replace(expression_phone, self.uer_info['管理人'], request_value)
        response = request(request_method, url=url, data=request_value)
        actual_result = response.json()
        do_excel.write_cell(
            'login',
            row,
            do_conf('ExcelNum', 'Actual_Column_Num'),
            response.text)
        try:
            self.assertEqual(expected, actual_result, msg='期望结果与实际结果不相等')
        except AssertionError as e:
            do_excel.write_cell(
                do_conf('SheetName', 'sheet_login'),
                row,
                do_conf('ExcelNum', 'Result_Column_Num'),
                do_conf('Result', 'result_fail'),
                color=RED)
            log.error('{}-测试[{}] :Failed\nDetails:\n{}'.format(inspect.stack()[0][3], title, e))
            raise e
        else:
            do_excel.write_cell(
                'login',
                row,
                do_conf('ExcelNum', 'Result_Column_Num'),
                do_conf('Result', 'result_pass'),
                color=GREEN)
            log.info('{}-测试[{}] :Passed'.format(inspect.stack()[0][3], title))
        log.info('执行登录-测试用例"{}"结束'.format(title))


if __name__ == '__main__':
    unittest.main()
