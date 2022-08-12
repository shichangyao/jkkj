# rsa加密处理
import rsa
import base64
from time import time

# 公钥加密
def rsaEncrypt(msg):
    server_pub_key = """
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
    O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
    tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
    kKlZFc8Br7SHtbL2tQIDAQAB
    -----END PUBLIC KEY-----
    """
    # 生成公钥对象
    pub_key_byte = server_pub_key.encode('utf-8')
    # print(pub_key_byte)
    pub_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)

    # 要加密的数据转换成字节对象
    content = msg.encode('utf-8')

    # 加密，返回加密文本
    cryto_msg = rsa.encrypt(content,pub_key_obj)
    # base64编码
    cipher_base64 = base64.b64encode(cryto_msg)
    # 转成字符串
    return cipher_base64.decode()

def generator_sign(token):
    # 获取token的前50位
    print(token)
    token_50 = token[:50]
    # 生成时间戳
    timestamp = int(time())
    # print(timestamp)
    # 拼接
    msg = token_50 + str(timestamp)
    # print(msg)
    sign = rsaEncrypt(msg)
    return sign,timestamp



if __name__ == "__main__":
    import requests

    headers = {'X-Lemonban-Media-Type': 'lemonban.v3',"Content-Type":"application/json"}
    # 登录接口
    login_url = "http://api.lemonban.com/futureloan/member/login"
    login_data = {
        "mobile_phone": "13845467789",
        "pwd": "1234567890"
    }
    response = requests.request("POST", login_url, json = login_data,headers=headers)
    # print(response.json())
    token = response.json()["data"]["token_info"]["token"]
    # print(token)
    member_id = response.json()["data"]["id"]

    headers['Authorization'] = "Bearer {}".format(token)
    sign,timestamp = generator_sign(token)
    print("签名为:",sign,"\n时间戳为：",timestamp)

    recharge_url = "http://api.lemonban.com/futureloan/member/recharge"
    recharge_data = {"member_id": member_id, "amount": 2000,"sign":sign,"timestamp":timestamp}
    response = requests.request("POST", recharge_url,json=recharge_data,headers=headers )
    print(response.json())