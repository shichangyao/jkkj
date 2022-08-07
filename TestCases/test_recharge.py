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

import unittest,jsonpath
from Common.random_phone import get_old_phone
from Common.requests_encapsulation import send_requests

class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        '''
        登录接口调用,得到id、token设置为类属性
        '''
        # 拿到用户名和密码
        user,password = get_old_phone()
        # 登录接口调用
        resp = send_requests('POST','/member/login',{'mobile_phone':user,'pwd':password})
        print('响应结果：{}'.format(resp.text))
        # 得到id和token
        cls.id = jsonpath.jsonpath(resp.json(),'$..id')[0]
        cls.token = jsonpath.jsonpath(resp.json(),'$..token')[0]

    def test_recharge(self):
        print(self.id)
        print(self.token)