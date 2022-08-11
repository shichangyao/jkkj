'''
业务流（场景）
注册   用户名和密码
登录   同一用户名和密码
充值   上一个登录接口返回值里的token、member_id
提现   登录接口返回值里的token、member_id
加标
'''
import unittest

import ddt

from Common.random_phone import get_new_phone
from Common.handle_data import EnvData,replace_case_by_regular,clear_EnvData_attrs
from Common.handle_path import testdata_dir
from Common.read_excel import ReadExcel
from Common import myddt
from Common.requests_encapsulation import send_requests
from Common.handle_extract_data_from_response import extract_data_from_response

he = ReadExcel(testdata_dir+"/api_cases.xlsx","业务流")
cases = he.read_data()
he.close_file()

@myddt.ddt
class TestUserBusiness(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 清理环境变量EnvData里设置的类属性(如果先实例化EnvData,再调用为对象属性就不用清理)
        clear_EnvData_attrs()
        # 生成一个新的手机号
        new_phone = get_new_phone()
        setattr(EnvData,"phone",new_phone)

    @myddt.data(*cases)
    def test_user_business(self,case):
        # 第一步：替换数据
        case = replace_case_by_regular(case)

        # 发起请求，判断是否需要token
        if hasattr(EnvData,"token"):
            response = send_requests(case['method'],case['url'],case['request_data'],token = EnvData.token)
        else:
            response = send_requests(case['method'], case['url'], case['request_data'])
        # 判断是否有需要提取的数据，提取数据并设置为环境变量
        if case['expected']:
            extract_data_from_response(case["expected"],response.json())