"""
------------------------------------
@Time : 2019/6/1 14:21
@Auth : linux超
@File : test_Register_api.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest
import inspect
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
class TestRegisterApi(Base):
    """注册接口"""
    test_data = do_excel.get_name_tuple_all_value(do_conf('SheetName', 'sheet_register'))

    def setUp(self):
        log.info("开始执行测试用例")

    @data(*test_data)
    def test_register(self, value):
        row = value.CaseId + 1  # 用例ID所在行号
        precondition = value.Precondition  # 前置条件
        title = value.Title  # 用例标题
        url = BASE_URL + value.URL  # 用例url
        request_value = value.Data  # 请求参数
        request_method = value.Method  # 请求方法
        sql = value.Sql
        # 转json的目的是防止期望结果和实际结果的字符串形式匹配不上(excel 存储的期望结果有空格)
        expected = HandleJson.json_to_python(value.Expected)  # 期望结果
        expression_phone = do_conf('Expression', 'phone_number')  # 正则表达式
        if precondition != '手机号已被注册':
            phone = self.mysql.get_phone()
            request_value = do_replace(expression_phone, phone, request_value)
        else:
            phone = self.mysql(sql=sql, args=(1,))["MobilePhone"]  # 取数据表中第一行数据的MobilePhone
            request_value = do_replace(expression_phone, phone, request_value)
        response = request(request_method, url=url, data=request_value)
        actual_result = response.json()
        do_excel.write_cell(
            do_conf('SheetName', 'sheet_register'),
            row,
            do_conf('ExcelNum', 'Actual_Column_Num'),
            response.text)
        try:
            self.assertEqual(expected, actual_result, msg='期望结果与实际结果不相等')
        except AssertionError as e:
            do_excel.write_cell(
                do_conf('SheetName', 'sheet_register'),
                row,
                do_conf('ExcelNum', 'Result_Column_Num'),
                do_conf('Result', 'result_fail'),
                color=RED)
            log.error('{}-[{}] :Failed\nDetails:\n{}'.format(inspect.stack()[0][3], title, e))
            raise e
        else:
            do_excel.write_cell(
                do_conf('SheetName', 'sheet_register'),
                row,
                do_conf('ExcelNum', 'Result_Column_Num'),
                do_conf('Result', 'result_pass'),
                color=GREEN)
            log.info('[{}] :Passed'.format(title))

    def tearDown(self):
        log.info("测试用例执行结束")


if __name__ == '__main__':
    unittest.main()
