# 加标功能
'''
eval()和json.loads()区别
若变量中需要做一些加减等操作处理时，要用eval，可以将按照python语法执行，json.loads()不是
'''
import unittest
from Common.requests_encapsulation import send_requests
from Common.handle_extract_data_from_response import extract_data_from_response
from Common.mylogger import logger
from Common.read_excel import ReadExcel
from Common.handle_path import testdata_dir
from Common import myddt
from Common.handle_data import replace_case_by_regular,EnvData,clear_EnvData_attrs

he = ReadExcel(testdata_dir + '/api_cases.xlsx','加标')
cases = he.read_data()
he.close_file()

@myddt.ddt
class TestAdd(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("*********** 加标接口 开始测试 ***********")
        # 清理 EnvData里设置的属性
        clear_EnvData_attrs()
        # 调用登陆接口，得到token和member_id

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("*********** 加标接口 结束测试 ***********")

    @myddt.data(*cases)
    def test_add(self,case):
        # 1.替换case
        case = replace_case_by_regular(case)
        # 2.如果有前置sql  得到结果后再次替换
        # 3.发送请求，考虑用例是否用得到token
        if hasattr(EnvData,"admin_token"):
            response = send_requests(case['method'],case['url'],case["request_data"],token=EnvData.admin_token)
        else:
            response = send_requests(case['method'], case['url'], case["request_data"])
        # 4.如果有提取表达式，提取数据，设置为全局变量
        if case['extract_data']:
            extract_data_from_response(case['extract_data'],response.json())
        # 5.如果有期望，则添加断言;若有sql则执行数据库校验
        # if case['expected']:
        #