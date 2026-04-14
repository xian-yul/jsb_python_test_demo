# @Time         : 2024/02/05 上午 11:23
# @Author       : ljx
# @File         : requests_post.py
# @Software     : PyCharm
import json

import requests
from utils import util

# 值需放入sign进行md5加密 定义变量存储时间 保证时间一致
sess = requests.session()
time = util.timestamp()
phone = 18912340003
sendSms_url = "http://v3.www.jinsubao.test/api/sendSms?timestamp=" + str(time)
# 请求参数 放入body 传入var加密
body_var = f'{{"phone":"{phone}","smsType":"7"}}'
var = util.generate_var(body_var)
sk = util.generate_sk()
# 按排序加密sk>timestamp>var 参数不用进行加密 例如 phone
sign_data = f"sk={sk}&timestamp={time}&var={var}"
sign = util.MD5(sign_data)

# header信息
header = {
    "Sign": sign,
    "Content-Type": "application/json"
}

# 请求入参
data = {
    "phone": phone,
    "smsType": "7",
    "sk": str(sk),
    "var": str(var)
}

# 将数据转换成JSON格式字符串
json_data = json.dumps(data, ensure_ascii=False)
print(json_data)

# 使用requests发送post请求
request = sess.post(url=sendSms_url, headers=header, data=json_data)
print(f"请求url ： {request.url}")
print(f"请求结果 : {request.status_code}")
print(f"返回数据 : {request.text}")
print("发送验证码")

time = util.timestamp()
claim_url = "http://v3.www.jinsubao.test/api/promotion-activity-participation/claim?timestamp=" + str(time)
# 请求参数 放入body 传入var加密
body_var = f'{{"phone":"{phone}","activityId":"426","activitySharerId":"31","verifyCode":"666666"}}'
var = util.generate_var(body_var)
sk = util.generate_sk()

# 按排序加密sk>timestamp>var 参数不用进行加密 例如 phone
sign_data = f"sk={sk}&timestamp={time}&var={var}"
sign = util.MD5(sign_data)

# header信息
header = {
    "Sign": sign,
    "Content-Type": "application/json"
}

# 请求入参 - 使用字典字面量形式，提高可读性
data = {
    "activityId": "63",
    "activitySharerId": "31",
    "phone": phone,
    "verifyCode": "666666",
    "sk": str(sk),
    "var": str(var)
}
# 将数据转换成JSON格式字符串
json_data = json.dumps(data, ensure_ascii=False)
print(json_data)

# 使用requests发送post请求
request = sess.post(url=claim_url, headers=header, data=json_data)
print(f"请求url: {request.url}")
print(f"请求结果 : {request.status_code}")
print(f"返回数据 : {request.text}")
print("进行领取优惠券")
