import unittest,json
from Common import myddt
from Common.requests_encapsulation import send_requests
from Common.read_excel import ReadExcel
from Common.handle_path import testdata_dir
from Common.mylogger import logger
from Common.handle_db import HandleDB
from Common.random_phone import get_new_phone
from Common.handle_data import replace_mark_with_data

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
        # print(case)
        logger.info("执行用例{}：{}".format(case["id"], case["title"]))
        # case = cases[0]
        # 替换(动态)mobeil_phone和check_sql中的#phone#

        if case["request_data"].find('#phone#') != -1:
            new_phone = get_new_phone()
            case = replace_mark_with_data(case, '#phone#', new_phone)
            # 通过函数替换
            # case["request_data"] = case["request_data"].replace('#phone#',new_phone)
            # case["check_sql"] = case['check_sql'].replace('#phone#',new_phone)
        # # 将请求数据从json字符串转换成字典对象   这个被__pre_data方法替代
        # case["request_data"] = json.loads(case["request_data"])
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