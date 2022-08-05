'''
随机生成手机号码
1.随机生成11位手机号码
2.数据库校验是否存在
'''
import random
from Common.handle_db import HandleDB

prefix = [133,149,153,173,177,180,181,189,199,130,131,132,145,155,156,166,171,175,176,185,186,166,
          134,135,136,137,138,139,147,150,151,152,157,158,159,172,178,182,]

# one step:生成
def __generate_phone():
    index = random.randint(0,len(prefix)-1)
    phone = str(prefix[index])
    for i in range(0,8):
        phone += str(random.randint(0,9))
    return phone

# two step:校验
# 如果校验存在，需要重新生成
def get_new_phone():
    db = HandleDB()
    while True:
        # 生成
        phone = __generate_phone()
        # 校验
        count = db.get_count('select * from member where mobile_phone = "{}"'.format(phone))
        if count == 0:  # 如果没查到那就是没注册的号码
            db.get_close()
            return phone

print(get_new_phone())