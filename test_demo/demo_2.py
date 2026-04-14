# @Time         : 2024/02/05 上午 11:23
# @Author       : ljx
# @File         : requests_post.py
# @Software     : PyCharm
import datetime
import os
import requests
from dotenv import load_dotenv
from utils import util
from utils.util import generate_encryption_params
from concurrent.futures import ThreadPoolExecutor

# 加载环境变量文件
load_dotenv('/get_token.env')


def send_transfer_request(session):
    # 动态生成时间戳确保每次请求唯一
    time = util.timestamp()
    url = f"http://v3.www.jinsubao.test/portalCust/jstOrgAcct/transfer2Merc?timestamp={time}"
    # 转换为可读格式
    formatted_time = datetime.datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f"请求时间: {formatted_time}")
    # 统一使用字典表示请求体
    body_dict = {
        "accType": 1,
        "amount": 1,
        "password": "666666"
    }
    # 进行加密
    encryption_params = generate_encryption_params(body_dict,time)
    sk = encryption_params['sk']
    body_json = encryption_params['body_json']
    var = encryption_params['var']

    # 构建签名原文
    sign_data = f"sk={sk}&timestamp={time}&var={var}"
    sign = util.MD5(sign_data)

    # header信息（注意：实际项目中不应硬编码 token）
    header = {
        "Sign": sign,
        "Content-Type": "application/json",
        "Authorization": os.getenv("AUTH_TOKEN", "")
    }

    # 请求入参 - 使用原始字典对象
    data = {
        **(body_json if isinstance(body_json, dict) else {}),
        "sk": sk,
        "var": var
    }

    try:
        response = session.post(url=url, headers=header, json=data)
        print(f"请求url: {response.url}")
        print(f"请求结果 : {response.status_code}")
        print(f"返回数据 : {response.text}")

        if response.status_code != 200:
            print("警告：HTTP 请求失败！")
    except Exception as e:
        print(f"请求过程中出现异常：{e}")


# if __name__ == "__main__":
#     with requests.Session() as session:
#         for i in range(10):  # 删除多余的 i += 1
#             send_transfer_request(session)
#             print(f"第 {i + 1} 次请求")

def run_concurrent_test(num_threads=5, requests_per_thread=2):
    """运行并发测试"""

    def worker(thread_id):
        with requests.Session() as session:
            print(f"线程 {thread_id} 开始执行")
            for i in range(requests_per_thread):
                send_transfer_request(session)
                print(f"线程 {thread_id} 第 {i + 1} 次请求完成")

    # 使用线程池执行并发测试
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker, i) for i in range(num_threads)]
        # 等待所有线程完成
        for future in futures:
            future.result()


if __name__ == "__main__":
    run_concurrent_test(num_threads=5, requests_per_thread=10)
