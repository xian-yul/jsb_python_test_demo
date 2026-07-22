import allure

from config.env_config import EnvConfig
from flows.regular.regular_case import RegularFunctionsCase
import pytest

from flows.regular.regular_implement import RegularFunctionsImplement


class TestRegularFunctions:

    def setup_method(self):
        """每个测试方法执行前的初始化"""
        self.test_data = {}  # 每个测试使用独立的数据

    def teardown_method(self):
        """每个测试方法执行后的清理"""
        # 清理测试产生的数据
        pass

    def setup_class(cls):
        env = EnvConfig(env="test")
        cls.case = RegularFunctionsCase(env.base_url['OPERA_URL'])
        cls.user = RegularFunctionsImplement(cls.case)
        cls.token = None

    # @pytest.fixture
    def test_phone_login(self):
        allure.attach("测试手机号登录")
        response = self.user.user_phone_login()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_user_setting(self):
        allure.attach("测试查询账户安全信息")
        response = self.user.get_user_setting()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_set_password(self):
        allure.attach("测试进行设置密码")
        response = self.case.user_set_password()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_password_login(self):
        allure.attach("测试进行设置密码并密码登录")
        response = self.user.user_password_login()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_no_setpassword_login(self):
        allure.attach("测试进行密码登录")
        response = self.case.password_login()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_reset_password(self):
        allure.attach("测试重置密码")
        response = self.user.user_reset_password()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_update_phone(self):
        allure.attach("测试修改手机号")
        response = self.user.upd_user_phone()
        assert response is not None
        assert response.status_code == 200

    # @pytest.fixture
    def test_manual_appeal(self):
        allure.attach("测试人工申诉")
        response = self.case.user_manual_appeal()
        assert response is not None
        assert response.status_code == 200

    def test_user_butler_certification(self):
        allure.attach("测试E管家加入企业")
        response = self.user.user_butler_certification()
        assert response is not None
        assert response.status_code == 200

    def test_invitation_code(self):
        allure.attach("校验邀请码")
        response = self.user.verify_invite_code()
        assert response is not None
        assert response.status_code == 200

    def test_update_password(self):
        allure.attach("测试修改密码")
        response = self.user.user_update_password()
        assert response is not None
        assert response.status_code == 200

    def test_opera_rest_user(self):
        allure.attach("测试运营重置密码")
        response = self.user.opera_reset_user()
        assert response is not None
        assert response.status_code == 200

    def test_create_order(self,api_client):
        resp = api_client.post(
            "https://your-api.com/order",
            json={"sku": "A001", "qty": 1}
        )
        assert resp.status_code == 201


if __name__ == '__main__':
    # 运行当前目录下所有测试文件并生成allure报告
    pytest.main(['-v', '--tb=short', '--alluredir=./allure-results', '.'])
