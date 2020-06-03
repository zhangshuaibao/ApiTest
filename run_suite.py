import os

import pytest
from case.testcase import case_data, main_program, load_config_yaml
from lib.mysql_db import DB

case_name = load_config_yaml('case_name')


class TestCase(object):
    def setup_class(self):
        self.db = DB()
        self.sql_assert = load_config_yaml('sql_assert')

    @pytest.mark.parametrize('data', case_data(case_name))
    def test_main_case(self, data):
        """
        执行测试脚本
        :param data:测试用例|dict
        :return:
        """
        main_program(self, data)  # 调用封装好的主程序运行


if __name__ == "__main__":
    # pytest.main(['run_suite.py', '-s'])
    pytest.main(['run_suite.py', '-s', '--alluredir', './reports'])
    os.system('allure generate reports/ -o reports/html --clean')
    # send_email(setting.REPORT_PATG)
