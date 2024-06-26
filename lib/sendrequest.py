import logging
import requests

from lib.data_driven import data_association
from lib.utlis import get_test_url, replace_body, literal_eval_data


def send_requests(apidata):
    """
    分析测试用例自带参数、发送请求
    :param apidata: 测试用例
    :return:
    """

    try:
        # 从读取的表格中获取响应的参数作为传递
        method = apidata["get_type"]
        url = data_association(apidata['url']).replace("'", '').replace("'", '')
        if apidata["header"] == '':
            header = None
        else:
            header = literal_eval_data(data_association(apidata['header']))
        # 判断表内是否有测试数据
        if apidata["data"] == "":
            body_data = None
        else:
            data_excel = literal_eval_data(data_association(apidata['data']))
            body_data = replace_body(apidata, data_excel)  # 参数的值替换成最新的值

        logging.info('请求url:{}'.format(get_test_url('loc') + url))
        logging.info('请求头:{}'.format(header))
        logging.info('请求参数:{}'.format(body_data))
        s = requests.session()
        re = s.request(method=method, url=get_test_url('loc') + url, headers=header,
                       json=body_data)
        logging.info("页面返回信息：%s" % re.text)

        return re
    except Exception as error:
        logging.error("错误信息", error)


if __name__ == '__main__':
    case_dict = {'id': 3.0, 'get_type': 'post', 'interface': '相减接口', 'title': '参数正常-成功', 'header': '',
                 'precondition': '', 'url': '/less', 'data': "{'a': '${code}', 'b':2}", 'name': '', 'rule': '',
                 'expected': "{'code': 1000, 'msg': 'success', 'value': -3}", 'code': 1000.0, 'status': 200.0,
                 'msg': 'success'}

    re = send_requests(case_dict)
    print(re.url)
    print(re.json())
