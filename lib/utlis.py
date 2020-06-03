"""公共方法类"""
import ast
import codecs
import configparser
import logging
import smtplib
import unittest

import configparser as cparser
import xlrd
import yaml
from openpyxl import load_workbook
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import setting


class Excel:
    """
    初始化方法 参数type：为r是读取excel，为w是写入excel获取不同的实例，参数file_name是将要读取的文件
    """

    def __init__(self, type, file_name):
        """
        :param type: r:读 w:写
        :param file_name: 文件路径
        """
        # 读取excel
        if type == 'r':
            # 打开文件
            self.workbook = xlrd.open_workbook(file_name)
            # 获取到所有的sheet_names,sheet1,sheet2获取到所有，获取到的是一个list
            self.sheet_names = self.workbook.sheet_names()
            # 装载所有数据的list
            self.list_data = []
        # 写入excel
        elif type == 'w':
            self.filename = file_name
            self.wb = load_workbook(self.filename)
            self.ws = self.wb.active

    def read(self) -> list:
        # 根据sheet_name去读取用例，并获取文件的总行数获取到每行的内容
        for sheet_name in self.sheet_names:
            # 通过每个sheetname获取到每个页的内容
            sheet = self.workbook.sheet_by_name(sheet_name)
            # 获取总行数
            rosw = sheet.nrows
            # 根据总行数进行读取
            for i in range(0, rosw):
                rowvalues = sheet.row_values(i)
                # 讲每一行的内容添加进去
                self.list_data.append(rowvalues)
            #     去除大标题第一行进行切割处理
        # 将得到的excel数据返回进行处理
        return self.list_data

    def write(self, data):
        """
        数据写入ex表内
        :param data: 需要写入的数据：list
        :return:
        """
        self.ws.append(data)
        self.wb.save(self.filename)


def excel_dict(data):
    """
    1.将excel头部替换成英文的
    2.处理成json/dict格式
    """
    header = {
        '用例编号': 'id',
        '请求类型': 'get_type',
        '测试url': 'url',
        '参数名字': 'test_body',
        '参数值': 'test_value',
        '测试接口': 'interface',
        '用例标题': 'title',
        '请求数据': 'data',
        '断言路径': 'json_path',
        '预期结果': 'expected',
        '请求头': 'header',
        '返回代码': 'code',
        '状态码': 'status',
        '响应状态': 'msg',
        '前置条件': 'precondition',
        '全局变量名称': 'name',
        '全局匹配规则': 'rule',
        '执行sql': 'sql_statement'

    }
    head = []
    list_dict_data = []
    for d in data[1]:
        # 获取到英文的头部内容如果为中文，则替换成英文 进行改成一个k
        # 传入两个参数的作用是 查到则返回查到的数据查不到则返回传入的原数据
        d = header.get(d, d)
        # 将去除的头部英文装进list中
        head.append(d)
    # 获取到数据进行切片处理，0坐标为标题，1坐标是头部
    for b in data[2:]:
        # 头部和内容拼接为json串
        dict_data = {}
        for i in range(len(head)):
            # 之所以判断类型，如果不进行判断会出现str的错误，strip去除空格也有转str的用法
            if isinstance(b[i], str):
                dict_data[head[i]] = b[i].strip()
            else:
                dict_data[head[i]] = b[i]
        # list里面是字典格式
        list_dict_data.append(dict_data)
    return list_dict_data

def get_test_url(msg):
    """
    返回不同环境的rul地址
    :param msg: loc：本地环境 uat:uat环境 dev:开发环境
    :return: url
    """
    if msg == 'dev':
        return setting.BASE_URL_dev
    elif msg == 'uat':
        return setting.BASE_URL_uat
    elif msg == 'loc':
        return setting.BASE_URL


def read_config_ini(variable, conf_name='emailconf'):
    """
    返回配置文件内的数据
    :param conf_name: 配置文件内数据标题
    :param variable: 具体变量名
    :return: 返回配置的数据
    """
    cf = cparser.ConfigParser()
    cf.read(setting.CONFIG_JSON, encoding='UTF-8')
    if variable != 'receiver':
        var = cf.get(conf_name, variable)
    else:
        try:
            literal_eval_data(cf.get(conf_name, variable))
            return literal_eval_data(cf.get(conf_name, variable))
        except Exception:
            return cf.get(conf_name, variable)
    return var


def config_header_datas(header):
    """
    返回标题下的所有数据
    :return: 数据为 list格式
    """
    cp = configparser.ConfigParser(allow_no_value=True)
    cp.read(setting.CONFIG_JSON)
    data = cp.items(header)
    return data


def send_email(newfile):
    """
    将报告发送至指定邮箱地址
    :param newfile: 需要发送的报告路径
    :return:
    """

    if read_config_ini('email') != 'True':
        logging.info('发送邮件功能未打开，去config.ini内打开该功能')
        return

    # 打开文件
    f = open(newfile, 'rb')
    # 读取文件内容
    mail_body = f.read()
    # 关闭文件
    f.close()
    # 发送邮箱服务器
    smtpserver = read_config_ini('smtpserver')
    # 发送邮箱用户名/密码
    user = read_config_ini('user')
    password = read_config_ini('password')
    # 发送邮箱
    sender = read_config_ini('sender')
    # 多个接收邮箱，单个收件人的话，直接是receiver='XXX@163.com'
    receiver = read_config_ini('receiver')
    # 发送邮件主题
    subject = read_config_ini('subject')

    msg = MIMEMultipart('mixed')
    msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msg_html1)
    msg_html = MIMEText(mail_body, 'html', 'utf-8')
    msg_html["Content-Disposition"] = 'attachment; filename="TestReport.html"'
    msg.attach(msg_html)
    # 要加上msg['From']这句话，否则会报554的错误。
    # 要在163设置授权码（即客户端的密码），否则会报535
    msg['From'] = 'zxz_apitest@163.com'
    #    msg['To'] = 'XXX@doov.com.cn'
    # 多个收件人
    msg['To'] = ",".join(receiver)
    msg['Subject'] = Header(subject, 'utf-8')

    # 连接发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def load_config_yaml(key, key2=None):
    """
    读取yamlconfi内的数据
    :param key:
    :param key2:
    :return:
    """
    f = open(setting.yaml_config, 'r', encoding='utf-8')
    content = yaml.load(f, Loader=yaml.FullLoader)
    data = content.get(key)
    if key2 is None:
        f.close()
        return data
    else:
        f.close()
        return data.get(key2)


def wrete_type(msg=None):
    """
    初始化写入数据
    :return:
    """
    data = load_config_yaml('init_data', 'init')
    with codecs.open(setting.TEST_JSON, 'w', encoding='utf-8') as f:
        for i in data.keys():
            a = i
            data1 = {a: data[i]}
            f.write(str(data1))
            f.write('\r\n')


def skip_test_case(msg):
    """
    判断是否跳过该case
    :param msg:
    :return:
    """
    if msg == 'skip':
        @unittest.skip('skip testcase')
        def skip():
            pass

        skip()


def replace_body(apidata, data, msg=None):
    """
    判断是否需要替换请求参数内某个建的值
    :param self:
    :param apidata:  excel内数据
    :param data:  请求参数
    :return:  替换后的请求参数
    """

    msg_data = apidata['test_body']
    if msg is None:
        if msg_data != '':
            list_data = apidata['test_body'].split(',')

            test_value = apidata['test_value'].split(',')
            for i, a in zip(list_data, test_value):
                if a == 'del':
                    data.pop(i)
                else:
                    data[i] = a
    else:
        list_data = apidata['test_body'].split(',')
        test_value = apidata['test_value'].split(',')
        if list_data[0] == 'geo_infos':
            return '制定参数'

    return data


def literal_eval_data(data):
    expected = ast.literal_eval(data)
    return expected
