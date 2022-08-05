import unittest
from Common import myddt
from Common.requests_encapsulation import send_requests
from Common.read_excel import ReadExcel
from Common.handle_path import testdata_dir
from Common.mylogger import logger
from Common.handle_db import HandleDB

he = ReadExcel(testdata_dir + '/api_cases.xlsx', '注册')
cases = he.read_data()
he.close_file()
# for case in cases:
#     print(case)

db = HandleDB()

@myddt.ddt
class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("********注册模块用例开始执行********")

    @classmethod
    def tearDownClass(cls):
        logger.info("********注册模块用例执行结束********")

    @myddt.data(*cases)
    def test_register_ok(self,case):
        print(case)
        logger.info("执行用例{}：{}".format(case["id"], case["title"]))
        # case = cases[0]
        # 发起请求
        response = send_requests(case['method'],case['url'],case["request_data"])
        try:
            self.assertEqual(response.json()["code"], case["expected"]["code"])
            self.assertEqual(response.json()["msg"], case["expected"]["msg"])
            # 如果check_sql有值,说明要做数据库校验
            if case['check_sql']:
                result = db.get_one_data(case['check_sql'])
                self.assertIsNone(result)
        except AssertionError as e:
            logger.exception("断言失败,用例不通过")
            raise
        else:
            logger.info("断言成功，用例通过")