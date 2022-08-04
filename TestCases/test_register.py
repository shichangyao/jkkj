import unittest
from Common import myddt
from Common.requests_encapsulation import send_requests
from Common.read_excel import ReadExcel
from Common.handle_path import testdata_dir

he = ReadExcel(testdata_dir + '/api_cases.xlsx', '注册')
cases = he.read_data()
he.close_file()
# for case in cases:
#     print(case)

@myddt.ddt
class TestRegister(unittest.TestCase):

    @myddt.data(*cases)
    def test_register_ok(self,case):
        # case = cases[0]
        # 发起请求
        response = send_requests(case['method'],case['url'],case["request_data"])
        self.assertEqual(response.json()["code"],case["expected"]["code"])
        self.assertEqual(response.json()["msg"],case["expected"]["msg"])