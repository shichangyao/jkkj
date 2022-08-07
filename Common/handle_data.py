'''
处理替换数据（excel中的标识符替换成测试数据）
一条用例中可能涉及多处，可以遍历得到
'''


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

class EnvData:
    '''
    存储用例要使用到的数据。
    '''
    pass

