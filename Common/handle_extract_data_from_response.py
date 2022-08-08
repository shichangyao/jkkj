'''
从响应提取数据
'''
import jsonpath
from Common.handle_data import EnvData

ss = '{"member_id":"$..id","token":"$..token"}'
response = {'code': 0, 'msg': 'OK', 'data': {'id': 11060401, 'leave_amount': 0.0, 'mobile_phone': '18038683924', 'reg_name': '小柠檬', 'reg_time': '2022-08-07 10:52:47.0', 'type': 1, 'token_info': {'token_type': 'Bearer', 'expires_in': '2022-08-07 10:58:49', 'token': 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjExMDYwNDAxLCJleHAiOjE2NTk4NDExMjl9.rtHbbcazIARBItUWyo3MBsHd8rTCsLzB6FiqXheUSPwi4f_0iQcRta9VkvTF5Ik7CfieFrw1-7lifdm3MvNcIQ'}}, 'copyright': 'Copyright 柠檬班 © 2017-2019 湖南省零檬信息技术有限公司 All Rights Reserved'}

def extract_data_from_response(extract_exprs,response_dict):# 传入期望值和响应值
    """
    根据jsonpath提取表达式，从响应结果当中,提取数据并设置为环境变量EnvData类的属性，作为全局变量
    :param extract_exprs:从excel中读取出来的，提取表达式的字符串
    :param response_dict:http请求之后的响应结果
    :return:None
    """
    # 将提取的表达式转换成字典
    extract_dict = eval(extract_exprs)
    # 遍历字典,key作为全局变量名，value是jsonpath提取表达式
    for key,value in extract_dict.items():
        # 提取
        res = str(jsonpath.jsonpath(response_dict,value)[0])

        # 设置环境变量
        setattr(EnvData,key,res)


if __name__ == "__main__":
    ss = '{"member_id":"$..id","token":"$..token"}'
    response = {'code': 0, 'msg': 'OK',
                'data': {'id': 11060401, 'leave_amount': 0.0, 'mobile_phone': '18038683924', 'reg_name': '小柠檬',
                         'reg_time': '2022-08-07 10:52:47.0', 'type': 1,
                         'token_info': {'token_type': 'Bearer', 'expires_in': '2022-08-07 10:58:49',
                                        'token': 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjExMDYwNDAxLCJleHAiOjE2NTk4NDExMjl9.rtHbbcazIARBItUWyo3MBsHd8rTCsLzB6FiqXheUSPwi4f_0iQcRta9VkvTF5Ik7CfieFrw1-7lifdm3MvNcIQ'}},
                'copyright': 'Copyright 柠檬班 © 2017-2019 湖南省零檬信息技术有限公司 All Rights Reserved'}
    extract_data_from_response(ss,response)
    print(EnvData.__dict__)