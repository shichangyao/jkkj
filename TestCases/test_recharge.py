'''
充值接口:
    所有用例的前置：登录。拿到两个数据：id和token
    把前置数据传递给测试用例；
    充值接口的请求数据为：id，token
'''
'''
jsonpath相关
使用：jsonpath.jsonpath(字典对象，jsonpath表达式)  返回值为列表
jsonpath表达式可参考相关文档   eg:'$..id','$.data.token_info.token'
'''

import unittest,jsonpath,json
from Common.random_phone import get_old_phone
from Common.requests_encapsulation import send_requests
from Common.read_excel import ReadExcel
from Common.handle_path import testdata_dir
from Common import myddt
from Common.handle_data import replace_mark_with_data
from Common.mylogger import logger
from Common.handle_db import HandleDB

he = ReadExcel(testdata_dir + '/api_cases.xlsx',"充值")
cases = he.read_data()
he.close_file()

db = HandleDB()

@myddt.ddt
class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        '''
        登录接口调用,得到id、token设置为类属性
        '''
        # 拿到用户名和密码
        user,password = get_old_phone()
        logger.info("获取到的用户名和密码分别为：{}".format(user,password))
        # 登录接口调用
        resp = send_requests('POST','/member/login',{'mobile_phone':user,'pwd':password})
        logger.info("登录的响应结果为：{}".format(resp.text))
        # 得到id和token
        cls.member_id = jsonpath.jsonpath(resp.json(),'$..id')[0] # 此处有坑：定义类属性不能直接使用cls.id会报错，可能会重复
        logger.info("获取到的member_id值为：{}".format(cls.member_id))
        cls.token = jsonpath.jsonpath(resp.json(),'$..token')[0]
        logger.info("获取到的token值为：{}".format(cls.token))
        logger.info("********注册模块用例开始执行********")

    @classmethod
    def tearDownClass(cls):
        logger.info("********注册模块用例执行结束********")

    @myddt.data(*cases)
    def test_recharge(self,case):
        # 替换数据
        logger.info("执行用例{}：{}".format(case["case_id"], case["title"]))
        if case["request_data"].find('#member_id#') != -1:
            case = replace_mark_with_data(case,"#member_id#",str(self.member_id))
            logger.info("执行的测试用例数据为：{}".format(case))

        # 数据库查询当前leaveamount   (充值之前)
        if case['check_sql']:
            user_money_before_recharge = db.get_one_data(case['check_sql'])["cast(leave_amount as char)"]
            logger.info("充值前的余额为：{}".format(user_money_before_recharge))
            # 期望余额。充值之前+充值的金额
            recharge_money = json.loads(case['request_data'])['amount']
            logger.info("本次充值的余额为：{}".format(recharge_money))
            expected_user_leave_amount = round(float(user_money_before_recharge) + recharge_money,2)  # 此处避免浮点数计算出现多位小数的情况采用round处理
            logger.info("期望充值之后的余额为：{}".format(expected_user_leave_amount))
            # 更新期望结果---将更新的期望用户余额更新到期望结果当中
            case = replace_mark_with_data(case,"#money#",str(expected_user_leave_amount))

        # 发起请求,开始充值
        response = send_requests(case['method'],case['url'],case['request_data'],token = self.token)

        # 将期望结果转换成字典对象，在比对
        expected = json.loads(case["expected"])

        # 断言
        try:
            self.assertEqual(response.json()["code"], expected["code"])
            self.assertEqual(response.json()["msg"], expected["msg"])
            if case['check_sql']:
                self.assertEqual(response.json()['data']['id'],expected['data']['id'])
                self.assertEqual(response.json()['data']['leave_amount'],expected['data']['leave_amount'])
                # 数据库查询充值后的余额
                user_money_after_recharge = db.get_one_data(case['check_sql'])['cast(leave_amount as char)']
                logger.info("充值后的余额为：{}".format(user_money_after_recharge))
                self.assertEqual("{:.2f}".format(expected['data']['leave_amount']),"{:.2f}".format(float(user_money_after_recharge)))
        except AssertionError:
            logger.exception("断言失败！")
            raise
        else:
            logger.info("断言成功，用例通过")