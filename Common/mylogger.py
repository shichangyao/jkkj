import logging
from parser_config import conf


class MyLogger(logging.Logger):
    def __init__(self,name,level=logging.INFO,file=None):
        # 设置输出级别、输出渠道、输出日志格式
        super().__init__(name,level)
        # 日志格式
        fmt = '%(asctime)s %(name)s %(levelname)s %(filename)s-%(lineno)dline:%(message)s'
        formatter = logging.Formatter(fmt)

        # 控制台渠道
        handle = logging.StreamHandler()
        handle.setFormatter(formatter)
        self.addHandler(handle)

        if file:
            # 文件渠道
            handle2 = logging.FileHandler(file,encoding='utf-8')
            handle2.setFormatter(formatter)
            self.addHandler(handle2)

# 是否需要写入文件
if conf.getboolean('log','file_ok'):
    file_name = conf.get('log','file_name')
else:
    file_name = None

logger = MyLogger(conf.get("log","name"),conf.get("log","level"),file_name)

if __name__ == "__main__":
    mlogger = MyLogger(conf.get("log","name"),file="my_log.txt")
    mlogger.info('测试，封装的日志类！')



''''
0.日志收集器
1.日志名字
2.日志级别(LEVEL):DEBUG,INFO,WARNING,ERROR等等
3.输出渠道（包括格式）
4.日志内容
'''
# logger = logging.getLogger('ceshirizhi')
# # 设置日志级别
# logger.setLevel(logging.INFO)
# # 设置日志输出渠道
# handlel = logging.StreamHandler()
# # 设置渠道自己的输出级别
# handlel.setLevel(logging.ERROR)
#
# # 设置渠道的内容格式
# fmt = '%(asctime)s %(name)s %(levelname)s %(filename)s-%(lineno)dline:%(message)s'
# formatter = logging.Formatter(fmt)
#
# # 将日志格式绑定到渠道中
# handlel.setFormatter(formatter)
#
# # 将设置好的渠道，添加到日志收集器上
# logger.addHandler(handlel)
#
# # 添加filehandle
# handlel2 = logging.FileHandler('log.txt',encoding='utf-8')
# handlel2.setFormatter(formatter)
# logger.addHandler(handlel2)
#
# # logging的handels中有文件回滚可设置log大小和回滚方式
#
#
# logger.info('这是第一个收集器')
# logger.error('错误！！！')