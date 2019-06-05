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

from libs.ddt import (data, ddt)
from base.base import Base
from common.ParseExcel import do_excel
from common.DataReplace import register_login_parameters
from common.HandleJson import HandleJson
from common.ParseConfig import do_conf
from common.RecordLog import log


@ddt
class TestRegisterApi(Base):
    """注册接口"""
    test_data = do_excel.get_name_tuple_all_value(do_conf('SheetName', 'Register'))

    @data(*test_data)
    def test_register(self, value):
        row = value.CaseId + 1  # 用例ID所在行号
        title = value.Title  # 用例标题
        url = do_conf('URL', 'Host_Url') + value.URL  # 用例url
        request_value = value.Data  # 请求参数
        request_method = value.Method  # 请求方法
        log.info('开始执行注册-"{}"测试用例'.format(title))
        # 转json的目的是防止期望结果和实际结果的字符串形式匹配不上(excel 存储的期望结果有空格)
        expected = HandleJson.json_to_python(value.Expected)  # 期望结果
        not_exist_phone = self.mysql.get_not_exist_phone()  # 正向用例的注册账号
        request_value = register_login_parameters(not_exist_phone, request_value)
        response = self.request(request_method, url=url, data=request_value)
        actual_result = response.json()
        do_excel.write_cell(
            do_conf('SheetName', 'Register'),
            row,
            do_conf('ExcelNum', 'Actual_Column'),
            response.text)
        try:
            self.assertEqual(expected, actual_result, msg='测试{}失败'.format(title))
        except AssertionError as e:
            do_excel.write_cell(
                do_conf('SheetName', 'Register'),
                row,
                do_conf('ExcelNum', 'Result_Column'),
                do_conf('Result', 'Fail'),
                color=RED)
            log.error('{}-测试[{}] :Failed\nDetails:\n{}'.format(inspect.stack()[0][3], title, e))
            raise e
        else:
            do_excel.write_cell(
                do_conf('SheetName', 'Register'),
                row,
                do_conf('ExcelNum', 'Result_Column'),
                do_conf('Result', 'Pass'),
                color=GREEN)
            log.info('{}-测试[{}] :Passed'.format(inspect.stack()[0][3], title))
        log.info('执行注册-测试用例"{}"结束'.format(title))


if __name__ == '__main__':
    unittest.main()
