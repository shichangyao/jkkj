import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)

# 测试用例路径
testcase_dir = os.path.join(base_dir,'TestCases')
# 日志路径
logs_dir = os.path.join(base_dir,'Outputs/logs')
# 测试报告路径
reports_dir = os.path.join(base_dir,'Outputs/report')
# 测试数据路径
testdata_dir = os.path.join(base_dir,'TestDatas')
# 配置文件路径
conf_dir = os.path.join(base_dir,'Conf')
# print(conf_dir)