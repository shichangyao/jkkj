'''
基于项目定制化封装
1.鉴权token
2.项目通用的请求
    {'X-Lemonban-Media-Type': 'lemonban.v2'}
3.请求体格式:application/json
'''

import requests

def __handle_header(token=None):
    headers = {'X-Lemonban-Media-Type': 'lemonban.v2',"Content-Type":"application/json"}
    if token:
        headers['Authorization'] = "Bearer {}".format(token)
    return headers

def send_requests(method,url,data=None,token=None):
    # 拿到请求头
    headers = __handle_header(token)
    # 根据请求类型判断发送请求
    if method == 'GET':
        res = requests.get(url,data,headers=headers)
    else:
        res = requests.post(url,json=data,headers=headers)
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