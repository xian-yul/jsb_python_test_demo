import yaml
import time
import os
from typing import List, Dict, Any, Optional


def load_api_yaml(file_path: str) -> List[Dict[str, Any]]:
    """
    加载API YAML配置文件（支持多文档），并自动添加当前毫秒时间戳

    Args:
        file_path (str): YAML文件路径

    Returns:
        List[Dict[str, Any]]: API配置数据列表（已处理时间戳）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            docs = list(yaml.safe_load_all(file))
            validated_docs = []
            current_timestamp = int(time.time() * 1000)

            for doc in docs:
                if isinstance(doc, dict):
                    processed_doc = doc.copy()
                    for key, value in processed_doc.items():
                        if key.upper() == 'API_URL' and isinstance(value, str):
                            if value.endswith('timestamp='):
                                processed_doc[key] = value + str(current_timestamp)
                            elif '?' in value and 'timestamp=' not in value:
                                processed_doc[key] = value + '&timestamp=' + str(current_timestamp)
                            elif '?' not in value:
                                processed_doc[key] = value + '?timestamp=' + str(current_timestamp)
                    validated_docs.append(processed_doc)
                else:
                    print("警告: YAML文档不是字典格式，跳过该项")
            return validated_docs
    except Exception as e:
        print(f"加载YAML文件失败: {e}")
        return []


def load_yaml_configs(file_path: str) -> List[Dict[str, Any]]:
    """
    加载YAML配置文件（支持多文档），不处理时间戳

    Args:
        file_path (str): YAML文件路径

    Returns:
        List[Dict[str, Any]]: 配置数据列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            configs = list(yaml.safe_load_all(file))
            return [config for config in configs if isinstance(config, dict)]
    except Exception as e:
        print(f"加载YAML配置失败: {e}")
        return []


def load_yaml_data(file_path: str) -> Dict[str, Any]:
    """
    加载YAML文件并返回完整数据（单文档，不处理时间戳）

    Args:
        file_path (str): YAML文件路径

    Returns:
        Dict[str, Any]: YAML文件的完整数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"加载YAML文件失败: {e}")
        return {}


def get_config_by_index(configs: List[Dict[str, Any]], index: int) -> Optional[Dict[str, Any]]:
    """
    根据索引获取API配置

    Args:
        configs (List[Dict[str, Any]]): API配置列表
        index (int): 索引位置

    Returns:
        Optional[Dict[str, Any]]: API配置，索引无效返回None
    """
    if 0 <= index < len(configs):
        return configs[index]
    return None


def get_config_by_field(configs: List[Dict[str, Any]], field_name: str, field_value: Any) -> Optional[Dict[str, Any]]:
    """
    根据字段名和值获取API配置

    Args:
        configs (List[Dict[str, Any]]): API配置列表
        field_name (str): 字段名称（如 'API_NAME', 'METHOD' 等）
        field_value (Any): 字段值

    Returns:
        Optional[Dict[str, Any]]: 匹配的API配置，未找到返回None
    """
    for config in configs:
        if config.get(field_name) == field_value:
            return config
    return None


def get_config_by_name(configs: List[Dict[str, Any]], api_name: str) -> Optional[Dict[str, Any]]:
    """
    根据API名称获取配置（便捷方法）

    Args:
        configs (List[Dict[str, Any]]): API配置列表
        api_name (str): API名称

    Returns:
        Optional[Dict[str, Any]]: 匹配的API配置，未找到返回None
    """
    return get_config_by_field(configs, 'API_NAME', api_name)


def get_yaml_config_by_name(file_path: str, api_name: str) -> Optional[Dict[str, Any]]:
    """
    从YAML文件中根据API名称获取指定配置（自动加载文件）

    Args:
        file_path (str): YAML文件路径
        api_name (str): API名称

    Returns:
        Optional[Dict[str, Any]]: 匹配的API配置，未找到返回None
    """
    try:
        configs = load_api_yaml(file_path)
        return get_config_by_name(configs, api_name)
    except Exception as e:
        print(f"获取YAML配置失败: {e}")
        return None


def get_test_data_list(file_path: str) -> List[Dict[str, Any]]:
    """
    从YAML文件中获取所有测试数据列表（test_data字段）

    Args:
        file_path (str): YAML文件路径

    Returns:
        List[Dict[str, Any]]: 测试数据列表，每条数据可能包含不同的字段
    """
    try:
        data = load_yaml_data(file_path)
        test_data = data.get('test_data', [])
        return test_data if isinstance(test_data, list) else []
    except Exception as e:
        print(f"获取测试数据失败: {e}")
        return []


def get_test_data_by_description(file_path: str, description: str) -> Optional[Dict[str, Any]]:
    """
    根据描述从YAML文件中获取特定的测试数据

    Args:
        file_path (str): YAML文件路径
        description (str): 测试数据描述

    Returns:
        Optional[Dict[str, Any]]: 匹配的测试数据（包含所有字段），未找到返回None
    """
    try:
        test_data_list = get_test_data_list(file_path)
        for data in test_data_list:
            if data.get('description') == description:
                return data
        print(f"警告: 未找到描述为 '{description}' 的测试数据")
        return None
    except Exception as e:
        print(f"获取测试数据失败: {e}")
        return None


def get_test_data_params(file_path: str, description: str) -> Optional[Dict[str, Any]]:
    """
    根据描述获取测试数据中的请求参数（排除description和result等元数据字段）

    Args:
        file_path (str): YAML文件路径
        description (str): 测试数据描述

    Returns:
        Optional[Dict[str, Any]]: 纯请求参数字典，未找到返回None
    """
    try:
        test_data = get_test_data_by_description(file_path, description)
        if test_data:
            params = {k: v for k, v in test_data.items()
                      if k not in ['description', 'result']}
            return params
        return None
    except Exception as e:
        print(f"获取测试参数失败: {e}")
        return None


def get_all_test_data_params(file_path: str) -> List[Dict[str, Any]]:
    """
    获取所有测试数据的请求参数（排除description和result等元数据字段）

    Args:
        file_path (str): YAML文件路径

    Returns:
        List[Dict[str, Any]]: 请求参数列表，每个元素是纯请求参数字典
    """
    try:
        test_data_list = get_test_data_list(file_path)
        params_list = []
        for data in test_data_list:
            params = {k: v for k, v in data.items()
                      if k not in ['description', 'result']}
            params_list.append(params)
        return params_list
    except Exception as e:
        print(f"获取所有测试参数失败: {e}")
        return []


def get_yaml_field_value(file_path: str, field_name: str) -> Any:
    """
    从YAML文件中获取指定字段的值

    Args:
        file_path (str): YAML文件路径
        field_name (str): 字段名称

    Returns:
        Any: 字段值，未找到返回None
    """
    try:
        data = load_yaml_data(file_path)
        return data.get(field_name)
    except Exception as e:
        print(f"获取字段值失败: {e}")
        return None


def get_api_body(file_path: str, api_name: str) -> Optional[Dict[str, Any]]:
    """
    根据API名称获取请求体数据（Body）

    Args:
        file_path (str): YAML文件路径
        api_name (str): API名称

    Returns:
        Optional[Dict[str, Any]]: 请求体数据，未找到返回None
    """
    try:
        config = get_yaml_config_by_name(file_path, api_name)
        if config:
            body = config.get('Body') or config.get('BODY')
            return body if isinstance(body, dict) else None
        return None
    except Exception as e:
        print(f"获取请求体失败: {e}")
        return None


def print_api_info(apis: List[Dict[str, Any]]):
    """
    打印API信息

    Args:
        apis (List[Dict[str, Any]]): API数据列表
    """
    print(f"共找到 {len(apis)} 个API配置:")

    for i, api in enumerate(apis, 1):
        print(f"\n--- API {i} ---")
        api_name = api.get('API_Name') or api.get('API_NAME', '未知')
        print(f"接口名称: {api_name}")
        print(f"URL: {api.get('API_URL', '未知')}")
        print(f"请求方式: {api.get('METHOD', '未知')}")

        body = api.get('Body') or api.get('BODY', {})
        if isinstance(body, dict) and body:
            print("请求体:")
            for key, value in body.items():
                print(f"  {key}: {value}")


if __name__ == "__main__":
    yaml_file = "../datas/declared_value.yaml"

    print("=" * 60)
    print("示例1: 加载所有API配置")
    print("=" * 60)
    configs = load_api_yaml("../datas/regular.yaml")
    print(f"共加载 {len(configs)} 个API配置\n")

    print("=" * 60)
    print("示例2: 根据索引获取配置")
    print("=" * 60)
    config = get_config_by_index(configs, 0)
    if config:
        print(f"索引0的配置: {config.get('API_NAME')}\n")

    print("=" * 60)
    print("示例3: 根据字段获取配置")
    print("=" * 60)
    config = get_config_by_field(configs, 'API_NAME', '买家密码登录')
    if config:
        print(f"找到的配置: {config.get('API_NAME')}")
        print(f"URL: {config.get('API_URL')}\n")

    print("=" * 60)
    print("示例4: 根据API名称获取配置（便捷方法）")
    print("=" * 60)
    config = get_config_by_name(configs, '手机号登录')
    if config:
        print(f"找到的配置: {config.get('API_NAME')}")
        print(f"URL: {config.get('API_URL')}\n")

    print("=" * 60)
    print("示例5: 直接从文件根据名称获取配置")
    print("=" * 60)
    config = get_yaml_config_by_name("../datas/regular.yaml", '买家重置密码')
    if config:
        print(f"配置: {config.get('API_NAME')}")
        print(f"Body: {config.get('Body')}\n")

    print("=" * 60)
    print("示例6: 获取测试数据")
    print("=" * 60)
    test_data_list = get_test_data_list(yaml_file)
    print(f"共 {len(test_data_list)} 条测试数据")
    for data in test_data_list:
        print(f"  - {data.get('description')}")

    print("\n" + "=" * 60)
    print("示例7: 获取测试参数")
    print("=" * 60)
    params = get_test_data_params(yaml_file, "正常用户登录")
    if params:
        print(f"请求参数: {params}")

    print("\n" + "=" * 60)
    print("示例8: 获取所有测试参数")
    print("=" * 60)
    all_params = get_all_test_data_params(yaml_file)
    for i, params in enumerate(all_params, 1):
        print(f"参数组 {i}: {params}")

