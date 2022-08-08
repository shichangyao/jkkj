'''
处理替换数据（excel中的标识符替换成测试数据）
一条用例中可能涉及多处，可以遍历得到
'''
from Common.handle_config import conf
import re,json

def replace_case_by_regular(case):
    '''
    对excel中读取出来的整条测试用例，做全部替换
    包括url，request_data,expected,check_sql
    '''
    # # 遍历替换
    # for key,value in case.items():
    #     if value is not None and isinstance(value,str):  # 确保是个字符串
    #         case[key] = replace_case_by_regular(value)
    # return case
    # 全部替换
    # 把case字典(从excel中读取出来的一条用例)转换成字符串
    case_str = json.dumps(case)
    # 替换
    new_case = replace_by_regular(case_str)
    # 把替换的字符串转换成字典
    case_dict = json.loads(new_case)
    return case_dict

def replace_by_regular(data):
    '''
    将字符串当中,匹配#(.*?)#部分，替换对应的真实数据。
    真实数据来自于两个方向：配置文件data区域以及Envdata的动态类属性(其值的类型必须是字符串)
    data:字符串
    返回替换后的字符串
    '''
    res = re.findall('#(.*?)#',data)
    if res:
        for item in res:
            # 得到标识符对应的值
            try:
                value = conf.get('data',item)
            except:
                # 如果有的值需要在后面才能得到，则可以先不处理，到下一循环处理
                try:
                    value = getattr(EnvData,item)
                except AttributeError:
                    continue
            print(value)
            # 再去替换原来的值
            data = data.replace("#{}#".format(item),value)
    return data

def replace_mark_with_data(case,mark,real_data):
    '''
    case:excel中读取出来的一条测试用例，是个字典
    mark:excel中的数据的占位符，匹配数据的
    real_data:要替换的真实数据
    '''
    for key,value in case.items():
        if value is not None and isinstance(value,str):   # 判断值是否为空才能发现是否需要替换，而且要替换的是字符串
            if value.find(mark) != -1:
                case[key] = value.replace(mark,real_data)
    return case

# 定义一个环境变量类，可以动态设置类属性
class EnvData:
    '''
    存储用例要使用到的数据。
    '''
    pass

def clear_EnvData_attrs():
    # 清理EnvData里设置的属性
    values = dict(EnvData.__dict__.items())
    for key,value in values.items():
        if key.startswith("__"):
            pass
        else:
            delattr(EnvData,key)

# 新方法：正则来替换
# import re
#
# setattr(EnvData,'member_id',"135897456")
# setattr(EnvData,'user_money',"2500")
# setattr(EnvData,'user','15353703383')
# data = '{"member_id":#member_id#,"amount":600,money:#user_money#,username="#user#"}'
# res = re.findall('#(.*?)#',data)
# # print(res)
# # 标识对应的值来自于：1.环境变量；2.配置文件
# if res:
#     for item in res:
#         # 得到标识符对应的值
#         try:
#             value = conf.get('data',item)
#         except:
#             value = getattr(EnvData,item)
#         print(value)
#         # 再去替换原来的值
#         data = data.replace("#{}#".format(item),value)
#     print(data)

if __name__ == "__main__":
    case = {
        "method":"POST","url":"http://api.lemonban.com/futureloan/#phone#/member/register",
        "request_data":'{"mobile_phone":"#phone#","pwd":"123456789"}'
    }
    if case["request_data"].find("#phone#") != -1:
        case = replace_mark_with_data(case,'#phone#',"135246789")
    for key,value in case.items():
        print(key,value)