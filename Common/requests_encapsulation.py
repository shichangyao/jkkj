'''
基于项目定制化封装
1.鉴权token
2.项目通用的请求
    {'X-Lemonban-Media-Type': 'lemonban.v2'}
3.请求体格式:application/json
'''
'''
eval()和json.loads()区别
若变量中需要做一些加减等操作处理时，要用eval，可以将按照python语法执行，json.loads()不是
'''

import requests
from Common.mylogger import logger
from Common.handle_config import conf

def __pre_data(data):
    '''
    若数据为字符串则转换成字典
    '''
    if data is not None and isinstance(data,str):
        # 如果有null,则替换为None
        if data.find("null") != -1:
            data.replace("null","None")
        # 使用eval转成字典.eval过程中，如果表达式有涉及计算，会自动计算。
        data = eval(data)
    return data

def __pre_url(url):
    '''
    拼接url
    '''
    base_url = conf.get('server','base_url')
    if url.startswith('/'):
        return base_url + url
    else:
        return base_url + '/' + url

def __handle_header(token=None):
    headers = {'X-Lemonban-Media-Type': 'lemonban.v2',"Content-Type":"application/json"}
    if token:
        headers['Authorization'] = "Bearer {}".format(token)
    return headers

def send_requests(method,url,data=None,token=None):
    # 拿到请求头
    headers = __handle_header(token)
    # 拼接url
    url = __pre_url(url)
    # 请求数据的处理，若是字符串转换成字典
    data = __pre_data(data)
    logger.info("请求头为：{}".format(headers))
    logger.info("请求方法为：{}".format(method))
    logger.info("请求url为：{}".format(url))
    logger.info("请求数据为：{}".format(data))
    # 根据请求类型判断发送请求
    method = method.upper()  # 请求方法大写处理
    # 根据请求类型判断发送请求
    if method == 'GET':
        res = requests.get(url,data,headers=headers)
    else:
        res = requests.post(url,json=data,headers=headers)
    logger.info("响应状态码为：{}".format(res.status_code))
    logger.info("响应数据为：{}".format(res.json()))
    return res

if __name__ == "__main__":
    login_url = "http://api.lemonban.com/futureloan/member/login"
    login_data = {
        "mobile_phone": "13845467789",
        "pwd": "1234567890"
    }
    response = send_requests("POST",login_url,login_data)
    token = response.json()["data"]["token_info"]["token"]

    recharge_url = "http://api.lemonban.com/futureloan/member/recharge"
    recharge_data = {"member_id":16719,"amount":10500}
    response = send_requests("POST",recharge_url,recharge_data,token)
    print(response.json())