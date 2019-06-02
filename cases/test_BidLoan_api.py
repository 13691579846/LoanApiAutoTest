"""
------------------------------------
@Time : 2019/6/1 14:22
@Auth : linux超
@File : test_BidLoan_api.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import unittest
from openpyxl.styles.colors import RED, GREEN

from config.config import BASE_URL
from libs.ddt import (data, ddt)
from base.base import Base
from common.ParseExcel import do_excel
from common.SendRequests import request
from common.DataReplace import do_replace
from common.HandleJson import HandleJson
from common.ParseConfig import do_conf


@ddt
class TestBidLoanApi(Base):
    pass

if __name__ == '__main__':
    unittest.main()