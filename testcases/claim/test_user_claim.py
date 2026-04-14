import pytest

from config.env_config import EnvConfig
from flows.claim.claim_case import UserClaimCouponService


class TestUserClaim:
    def setup_method(self):
        """每个测试方法执行前的初始化"""
        self.test_data = {}  # 每个测试使用独立的数据

    def teardown_method(self):
        """每个测试方法执行后的清理"""
        # 清理测试产生的数据
        pass

    def setup_class(cls):
        env = EnvConfig(env="test")
        cls.user_claim_coupon = UserClaimCouponService(env.base_url['USER_URL'])
        cls.token = None

    @pytest.fixture
    def test_user_claim_coupon(self):
        """测试领取优惠券成功"""
        response = self.user_claim_coupon.user_claim()
        assert response is not None
        assert response.status_code == 200
