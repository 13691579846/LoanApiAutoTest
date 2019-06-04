"""
------------------------------------
@Time : 2019/6/1 14:21
@Auth : linux超
@File : test_Recharge_api.py
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
from common.DataReplace import do_replace
from common.HandleJson import HandleJson
from common.ParseConfig import (do_conf, do_user)
from common.RecordLog import log
from business.LoginApi import login
from common.SendRequests import request


@ddt
class TestRechargeApi(Base):
    """充值接口"""
    test_data = do_excel.get_name_tuple_all_value(do_conf('SheetName', 'Recharge'))

    @data(*test_data)
    def test_recharge(self, value):
        login.login_api(method='post',
                        url=do_conf('URL', 'Host_Url') + '/member/login',
                        data={"mobilephone": str(do_user('Invest', 'mobilephone')), "pwd": "123456"}
                        )
        row = value.CaseId + 1  # 用例ID所在行号
        title = value.Title  # 用例标题
        url = do_conf('URL', 'Host_Url') + value.URL  # 用例url
        request_value = value.Data  # 请求参数
        request_method = value.Method  # 请求方法
        select_sql = value.Sql  # 查询充值结果的sql语句
        replace_sql = do_replace.recharge_parameters_data(select_sql)
        recharge_expected = HandleJson.json_to_python(value.Expected)  # 期望结果
        log.info('执行充值-测试用例"{}"开始'.format(title))
        request_value = do_replace.recharge_parameters_data(request_value)
        before_amount = self.mysql(sql=replace_sql)['LeaveAmount']  # 充值前的金额
        response = request(request_method, url=url, data=request_value)
        after_amount = self.mysql(sql=replace_sql)['LeaveAmount']  # 充值后的金额
        actual_amount = str(after_amount - before_amount)  # 实际金额
        actual_code = response.json()['code']  # 实际code
        # 构造个实际结果的字典
        actual_result = dict(leaveamount=actual_amount, code=actual_code)
        do_excel.write_cell(
            do_conf('SheetName', 'Recharge'),
            row,
            do_conf('ExcelNum', 'Actual_Column'),
            HandleJson.python_to_json(actual_result)
        )
        try:
            self.assertEqual(recharge_expected, actual_result, msg='测试{}失败'.format(title))
        except AssertionError as e:
            do_excel.write_cell(
                do_conf('SheetName', 'Recharge'),
                row,
                do_conf('ExcelNum', 'Result_Column'),
                do_conf('Result', 'Fail'),
                color=RED)
            log.error('{}-测试[{}] :Failed\nDetails:\n{}'.format(inspect.stack()[0][3], title, e))
            raise e
        else:
            do_excel.write_cell(
                do_conf('SheetName', 'Recharge'),
                row,
                do_conf('ExcelNum', 'Result_Column'),
                do_conf('Result', 'Pass'),
                color=GREEN)
            log.info('{}-测试[{}] :Passed'.format(inspect.stack()[0][3], title))
        log.info('执行登录-测试用例"{}"结束'.format(title))


if __name__ == '__main__':
    unittest.main()
