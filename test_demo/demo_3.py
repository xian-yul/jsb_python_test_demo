# @Time         : 2024/02/05 上午 11:23
# @Author       : ljx
# @File         : requests_post.py
# @Software     : PyCharm
import datetime

import requests
from utils.util import generate_encryption_params, load_test_data, timestamp, MD5
import logging

#1 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 使用相对路径或者配置文件传入路径更合理
DATA_FILE_PATH = '../datas/case.yaml'  # 假设项目根目录下


def build_sign(sk: str, timestamp: int, var: str) -> str:
    """构建签名"""
    sign_data = f"sk={sk}&timestamp={timestamp}&var={var}"
    return MD5(sign_data)


def send_transfer_request(session):
    try:
        test_data = load_test_data(DATA_FILE_PATH)
    except Exception as e:
        logging.error(f"加载测试数据失败: {e}")
        return

    for case in test_data:
        # 动态生成时间戳确保每次请求唯一
        time = timestamp()
        url = case['url'] + str(time)
        method = case['method']

        # 转换为可读格式
        try:
            formatted_time = datetime.datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logging.warning(f"时间戳转换失败: {e}")
            formatted_time = "Invalid Time"

        logging.info(f"请求时间: {formatted_time}")

        # 进行加密
        try:
            encryption_params = generate_encryption_params(case['request_data'])
        except Exception as e:
            logging.error(f"加密过程出错: {e}")
            continue

        sk = encryption_params.get('sk')
        body_json = encryption_params.get('body_json', {})
        var = encryption_params.get('var')
        sign = encryption_params.get('sign')

        if not all([sk, var]):
            logging.warning("缺少必要参数 sk 或 var，跳过当前请求")
            continue
        # header信息
        header = {
            "Sign": sign,
            "Content-Type": "application/json",
        }

        # 请求入参 - 使用原始字典对象
        data = {
            **(body_json if isinstance(body_json, dict) else {}),
            "sk": sk,
            "var": var
        }

        try:
            response = session.request(method=method, url=url, headers=header, json=data)
            logging.info(f"请求url: {response.url}")
            logging.info(f"请求结果 : {response.status_code}")
            logging.info(f"返回数据 : {response.text}")

            if response.status_code != 200:
                logging.warning("警告：HTTP 请求失败！")
        except requests.RequestException as e:
            logging.error(f"网络请求异常: {e}")
        except Exception as e:
            logging.error(f"未知异常: {e}")


if __name__ == "__main__":
    with requests.Session() as session:
        send_transfer_request(session)
