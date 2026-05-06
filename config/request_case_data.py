import json

from utils.util import generate_encryption_params
import time
from typing import List, Dict, Any, Optional


def prepare_request_data(config: Dict[str, Any], extra_params: Optional[Dict] = None,
                         extra_body: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
    """
    准备单个请求数据（使用Body或单条test_data）

    Args:
        config: API配置
        extra_params: 额外的URL参数
        extra_body: 额外的body参数

    Returns:
        单个请求数据字典
    """
    if not config:
        return None

    timestamp = int(time.time() * 1000)
    name = config['API_NAME']

    api_url = config['API_URL']
    if 'timestamp=' in api_url:
        url = api_url
    else:
        url = api_url + ('&' if '?' in api_url else '?') + f'timestamp={timestamp}'

    method = config['METHOD']

    body = config.get('Body') or config.get('BODY') or {}

    if not isinstance(body, dict):
        body = {}

    if extra_body:
        body = {**body, **extra_body}

    if extra_params:
        for key, value in extra_params.items():
            url = url.replace(f'{{{key}}}', str(value))

    encryption_params = generate_encryption_params(body, timestamp)
    sk = encryption_params.get('sk')
    body_json = encryption_params.get('body_json')
    var = encryption_params.get('var')
    sign = encryption_params.get('sign')

    data = {
        **(json.loads(body_json) if isinstance(body_json, str) else (body_json or {})),
        "sk": sk,
        "var": var
    }

    headers = config.get('headers') or config.get('Headers', {})
    if headers is None:
        headers = {}
    headers['sign'] = sign

    return {
        'method': method,
        'url': url,
        'data': data,
        'headers': headers,
        'name': name
    }


def prepare_request_data_list(config: Dict[str, Any], extra_params: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    准备请求数据列表（支持test_data多组数据）

    Args:
        config: API配置（包含test_data字段）
        extra_params: 额外的URL参数

    Returns:
        请求数据列表，每组test_data生成一个请求
    """
    if not config:
        return []

    test_data_list = config.get('test_data')

    if not test_data_list or not isinstance(test_data_list, list):
        single_data = prepare_request_data(config, extra_params)
        return [single_data] if single_data else []

    request_list = []
    timestamp = int(time.time() * 1000)
    name = config['API_NAME']

    # ⭐ 从 config 获取原始 URL（去掉 load_api_yaml 添加的时间戳）
    api_url = config['API_URL']
    # 移除已存在的时间戳参数
    import re
    clean_url = re.sub(r'[?&]timestamp=\d+', '', api_url)
    # 重新添加时间戳
    url_base = clean_url.rstrip('?').rstrip('&')
    url_template = url_base + ('&' if '?' in url_base else '?') + 'timestamp='

    method = config['METHOD']
    base_headers = config.get('headers') or config.get('Headers', {})
    if base_headers is None:
        base_headers = {}

    base_body = config.get('Body') or config.get('BODY') or {}
    if not isinstance(base_body, dict):
        base_body = {}

    for test_data in test_data_list:
        if not isinstance(test_data, dict):
            continue

        # ⭐ 拼接 URL 和时间戳
        url = url_template + str(timestamp)

        if extra_params:
            for key, value in extra_params.items():
                url = url.replace(f'{{{key}}}', str(value))

        params = {k: v for k, v in test_data.items()
                  if k not in ['description', 'result']}

        merged_params = {**base_body, **params}

        encryption_params = generate_encryption_params(merged_params, timestamp)
        sk = encryption_params.get('sk')
        body_json = encryption_params.get('body_json')
        var = encryption_params.get('var')
        sign = encryption_params.get('sign')

        data = {
            **(json.loads(body_json) if isinstance(body_json, str) else (body_json or {})),
            "sk": sk,
            "var": var
        }

        headers = base_headers.copy()
        headers['sign'] = sign

        request_list.append({
            'method': method,
            'url': url,
            'data': data,
            'headers': headers,
            'name': name,
            'test_description': test_data.get('description', '')
        })

    return request_list


if __name__ == "__main__":
    test_config = {
        'API_NAME': '手机号登录',
        'API_URL': '/api/login?timestamp=',
        'METHOD': 'POST',
        'test_data': [
            {
                'phone': 17200000005,
                'loginType': 1,
                'verifyCode': 666666,
                'description': '正常用户登录',
                'result': 200
            },
            {
                'phone': 17200000006,
                'loginType': 1,
                'verifyCode': 666666,
                'description': '新用户登录',
                'result': 200
            }
        ],
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    print("=" * 60)
    print("测试: prepare_request_data_list")
    print("=" * 60)
    request_list = prepare_request_data_list(test_config)
    print(f"生成了 {len(request_list)} 个请求:\n")

    for i, req in enumerate(request_list, 1):
        print(f"请求 {i}:")
        print(f"  描述: {req.get('test_description')}")
        print(f"  方法: {req['method']}")
        print(f"  URL: {req['url']}")
        print(f"  数据: {req['data']}")
        print()

