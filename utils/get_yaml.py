import yaml
import time
from typing import List, Dict, Any


def load_api_yaml(file_path: str) -> List[Dict[str, Any]]:
    """
    加载API YAML配置文件，并自动添加当前毫秒时间戳

    Args:
        file_path (str): YAML文件路径

    Returns:
        List[Dict[str, Any]]: API配置数据列表（已处理时间戳）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            docs = list(yaml.safe_load_all(file))
            # 校验每个文档是否为字典并添加时间戳
            validated_docs = []
            # 获取当前毫秒时间戳
            current_timestamp = int(time.time() * 1000)

            for doc in docs:
                if isinstance(doc, dict):
                    # 处理时间戳
                    processed_doc = doc.copy()
                    for key, value in processed_doc.items():
                        if key.upper() == 'API_URL' and isinstance(value, str):
                            if value.endswith('timestamp='):
                                processed_doc[key] = value + str(current_timestamp)
                            elif '?' in value and not 'timestamp=' in value:
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

        # 打印请求体
        body = api.get('Body') or api.get('BODY', {})
        if isinstance(body, dict) and body:
            print("请求体:")
            for key, value in body.items():
                print(f"  {key}: {value}")


# 使用示例
if __name__ == "__main__":
    # 读取YAML文件（自动处理时间戳）
    apis = load_api_yaml("../datas/claim.yaml")

    # 打印API信息
    print_api_info(apis)
