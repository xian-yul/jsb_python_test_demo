import os

from dotenv import load_dotenv

from config.request_api import BaseTestCase
from utils.log import Log

log = Log()
load_dotenv('E:\\jsb_python_test_demo\\get_token.env')


class DeclaredValueCase(BaseTestCase):
    """声明价值测试类"""

    def _get_default_yaml_path(self) -> str:
        """重写默认YAML路径"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "..", "..", "datas", "declared_value.yaml")

    def test_demo(self):
        """
        测试示例 - 执行买家密码登录测试
        """
        results = self.execute_api_test('买家密码登录')
        self.print_test_summary(results)
        return results


if __name__ == "__main__":
    BASE_URL = "http://v3.www.jinsubao.test"

    log.info("=" * 60)
    log.info("开始执行 test_demo 测试")
    log.info("=" * 60)

    case = DeclaredValueCase(base_url=BASE_URL)
    case.test_demo()

