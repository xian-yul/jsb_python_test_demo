# E:\jsb_python_test_demo\flows\base_test_case.py
import os
from typing import List, Dict, Any, Optional, Callable

from config.request_handler import RequestHandler
from utils.get_yaml import load_api_yaml, get_config_by_index, get_config_by_field
from utils.log import Log

log = Log()


class BaseTestCase:
    """
    测试用例基类 - 提供通用的API测试功能
    """

    def __init__(self, base_url: str, yaml_file_path: str = None):
        """
        初始化测试类

        Args:
            base_url: API基础URL
            yaml_file_path: YAML配置文件路径（可选）
        """
        self.client = RequestHandler(base_url)
        self.yaml_file_path = yaml_file_path or self._get_default_yaml_path()
        self.api_configs = self._load_api_configs()

    def _get_default_yaml_path(self) -> str:
        """获取默认YAML文件路径（子类可重写）"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "..", "datas", "default.yaml")

    def _load_api_configs(self) -> List[Dict[str, Any]]:
        """加载所有API配置"""
        return load_api_yaml(self.yaml_file_path)

    def _get_api_config(self, index: int) -> Optional[Dict[str, Any]]:
        """根据索引获取API配置"""
        return get_config_by_index(self.api_configs, index)

    def _get_api_config_by_field(self, field_name: str, field_value: Any) -> Optional[Dict[str, Any]]:
        """根据字段名和值获取API配置"""
        return get_config_by_field(self.api_configs, field_name, field_value)

    def _get_api_config_by_name(self, api_name: str) -> Optional[Dict[str, Any]]:
        """根据API名称获取配置（便捷方法）"""
        return self._get_api_config_by_field('API_NAME', api_name)

    def _execute_single_request(self, request_data: Dict[str, Any], index: int) -> Dict[str, Any]:
        """
        执行单个请求

        Args:
            request_data: 请求数据字典
            index: 请求序号

        Returns:
            测试结果字典
        """
        description = request_data.get('test_description', f'测试数据{index}')
        log.info(f"\n{'=' * 60}")
        log.info(f"执行第 {index} 组测试: {description}")
        log.info(f"{'=' * 60}")

        try:
            response = self.client.request(
                request_data['method'],
                request_data['url'],
                json=request_data['data'],
                headers=request_data['headers']
            )

            result = {
                'index': index,
                'description': description,
                'response': response,
                'status_code': response.status_code if response else None,
                'success': response and 200 <= response.status_code < 300
            }

            log.info(f"状态码: {result['status_code']}")
            if response:
                log.info(f"响应结果: {response.text[:500]}")

            return result

        except Exception as e:
            log.error(f"请求异常: {str(e)}")
            return {
                'index': index,
                'description': description,
                'response': None,
                'status_code': None,
                'success': False,
                'error': str(e)
            }

    def execute_api_test(self, api_name: str, prepare_data_func: Callable = None) -> List[Dict[str, Any]]:
        """
        通用方法 - 执行指定API的所有测试数据

        Args:
            api_name: API名称
            prepare_data_func: 准备请求数据的函数（可选），默认为 None

        Returns:
            测试结果列表
        """
        from config.request_case_data import prepare_request_data_list

        config = self._get_api_config_by_name(api_name)
        if not config:
            log.error(f"未找到API配置: {api_name}")
            return []

        request_data_list = prepare_request_data_list(config)
        if not request_data_list:
            log.error("未生成请求数据")
            return []

        log.info(f"API: {api_name} - 共找到 {len(request_data_list)} 组测试数据")

        results = [
            self._execute_single_request(req_data, i)
            for i, req_data in enumerate(request_data_list, 1)
        ]

        success_count = sum(1 for r in results if r['success'])
        log.info(f"\n{'=' * 60}")
        log.info(f"测试完成 - 总计: {len(results)}, 成功: {success_count}, 失败: {len(results) - success_count}")
        log.info(f"{'=' * 60}")

        return results

    def execute_single_api(self, api_name: str, extra_body: Dict = None, extra_params: Dict = None) -> Optional[Any]:
        """
        执行单个API请求（使用Body）

        Args:
            api_name: API名称
            extra_body: 额外的body参数
            extra_params: 额外的URL参数

        Returns:
            响应对象
        """
        from config.request_data import prepare_request_data

        config = self._get_api_config_by_name(api_name)
        if not config:
            log.error(f"未找到API配置: {api_name}")
            return None

        request_data = prepare_request_data(config, extra_params=extra_params, extra_body=extra_body)
        if not request_data:
            log.error("未生成请求数据")
            return None

        log.info(f"执行: {request_data['name']}")

        try:
            response = self.client.request(
                request_data['method'],
                request_data['url'],
                json=request_data['data'],
                headers=request_data['headers']
            )
            return response
        except Exception as e:
            log.error(f"请求异常: {str(e)}")
            return None

    def print_test_summary(self, results: List[Dict[str, Any]]) -> None:
        """
        打印测试结果汇总

        Args:
            results: 测试结果列表
        """
        log.info("\n" + "=" * 60)
        log.info("测试结果汇总:")
        log.info("=" * 60)

        for result in results:
            status = "✅ 成功" if result['success'] else "❌ 失败"
            log.info(f"{result['index']}. {result['description']}: {status} (状态码: {result['status_code']})")

            if not result['success'] and 'error' in result:
                log.error(f"   错误信息: {result['error']}")

        success_count = sum(1 for r in results if r['success'])
        log.info(f"\n总计: {len(results)} | 成功: {success_count} | 失败: {len(results) - success_count}")

