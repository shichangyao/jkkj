# 数据库校验
'''
1.数据库连接con   设定游标cur
2.获取一条数据   获取条数
3.获取所有数据
4.关闭数据库连接
'''
import pymysql
from Common.handle_config import conf

class HandleDB:
    def __init__(self):
        # 连接数据库,创建游标
        self.con = pymysql.connect(
            host=conf.get("mysql","host"),
            port=conf.getint("mysql","port"),
            user=conf.get("mysql","user"),
            password=conf.get("mysql","password"),
            database=conf.get("mysql","database"),
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.con.cursor()

    def get_one_data(self,sql):
        self.con.commit()
        self.cur.execute(sql)
        self.con.ping(reconnect=True)  # # 检查连接是否断开，如果断开就进行重连
        return self.cur.fetchone()

    def get_all_datas(self,sql):
        self.con.commit()
        self.con.ping(reconnect=True)
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_count(self,sql):
        self.con.commit()
        self.con.ping(reconnect=True)
        return self.cur.execute(sql)

    def update(self,sql):
        '''
        对数据库进行增删改
        '''
        self.con.ping(reconnect=True)
        self.cur.execute(sql)
        self.con.commit()

    def get_close(self):
        self.cur.close()
        self.con.close()

if __name__ == "__main__":
    # sql = "select * from member limit 3"
    # db = HandleDB()
    # # count = db.get_count(sql)
    # # print(count)
    # datas = db.get_all_datas(sql)
    # print(datas)
    # db.get_close()
    db = HandleDB()
    sql = 'select * from member where mobile_phone = "15012345678"'
    # 发送一个请求
    from Common.requests_encapsulation import send_requests

    case = {
        'method':'POST',
        'url':'http://api.lemonban.com/futureloan/member/register',
        'request_data':{"mobile_phone":"15012345678","pwd":"123456789","type":"1","reg_name":"可爱的老六"}
    }
    response = send_requests(case['method'],case['url'],case['request_data'])
    print("响应结果为：",response.json())
    # 查询注册的手机号码
    count = db.get_count(sql)
    print("获取到的结果为：",count)