import json

from utils.util import generate_encryption_params
import time


def prepare_request_data(config, extra_params=None, extra_body=None):
    """准备请求数据的公共方法，支持灵活传参"""
    if not config:
        return None

    timestamp = int(time.time() * 1000)
    name = config['API_NAME']
    url = config['API_URL'] + str(timestamp)
    method = config['METHOD']
    body = config['Body'] or {}

    # 合并额外的body参数
    if extra_body:
        body = {**body, **extra_body}

    # 处理URL参数替换
    if extra_params:
        for key, value in extra_params.items():
            url = url.replace(f'{{{key}}}', str(value))  # 支持 {param} 占位符
    print(body)
    encryption_params = generate_encryption_params(body, timestamp)
    sk = encryption_params.get('sk')
    body_json = encryption_params.get('body_json')
    var = encryption_params.get('var')
    sign = encryption_params.get('sign')

    # 请求入参 - 使用原始字典对象
    data = {
        **(json.loads(body_json) if isinstance(body_json, str) else (body_json or {})),
        "sk": sk,
        "var": var
    }

    headers = config['headers'] or config.get('Headers', {})
    headers['sign'] = sign

    return {
        'method': method,
        'url': url,
        'data': data,
        'headers': headers,
        'name': name
    }
