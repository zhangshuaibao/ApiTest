import os

BASE_URL = "http://127.0.0.1:8100"
BASE_URL_dev = 'http://127.0.0.1:8100'
BASE_URL_uat = 'http://127.0.0.1:8100'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

case_root = os.path.join(PROJECT_ROOT, 'database')  # 测试用例
LOG_PATH = os.path.join(PROJECT_ROOT, 'log', 'api_test.log')  # 日志
REPORT_PATG = os.path.join(PROJECT_ROOT, 'reports', 'index.html')  # 日志
TEST_JSON = os.path.join(PROJECT_ROOT, 'database', 'testData')  # 存放接口返回数据
CONFIG_JSON = os.path.join(PROJECT_ROOT, 'database', 'config.ini')  # 配置文件路径
yaml_config = os.path.join(PROJECT_ROOT, 'database','configuration.yaml')  # yaml
