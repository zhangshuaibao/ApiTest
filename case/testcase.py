import json

from jsonpath import jsonpath
from lib.data_driven import write_data
from lib.sendrequest import send_requests
from lib.utlis import *
from setting import case_root


def case_data(dataname) -> list:
    """
    处理测试用例数据
    :param dataname: 测试用例文件名
    :return: 测试用例数据
    """
    test_case = case_root + '/{}.xlsx'.format(dataname)
    test_num = Excel('r', test_case).read()
    testdata = excel_dict(test_num)
    return testdata


def main_program(self, data):
    """
    执行测试脚本
    :param data: 参数化后测试用例|dict类型
    :return:
    """
    preposition = data['precondition']
    # 如果用例编号为1，执行初始化写入没
    if data.get('id') == 1:
        wrete_type(preposition)
    # 判断是否跳过该用例
    skip_test_case(preposition)
    response = send_requests(data)
    result = response.json()
    rule = data['rule']
    name = data['name']
    status = data['status']
    msg = data['msg']
    sql_data = data.get('sql_statement')
    # 当name不为空时，表示有全局变量需要写入
    if name != '':
        write_data(name, result, rule)
    # self.sql_assert 为configuration.yaml里的配置
    if sql_data != '' and self.sql_assert is True:
        logging.info('sql语句为{}'.format(sql_data))
        sql = self.db.get(sql_data)[0].get('id')
        logging.info('查询结果为{}'.format(sql))
    assert response.status_code == status
    assert result['message'] == msg
    json_path = data['json_path']
    if json_path != '':
        path_list = json_path.split(',')
        expected_list = data['expected'].split(',')
        for p, e in zip(path_list, expected_list):
            if p.startswith('$'):
                res = str(jsonpath(result, p)[0])
                assert res == e, f'json path:{p}>Actual:{res}!=expected:{e}'
