import os

import yaml
import time
from config.request_handler import RequestHandler
from flows.request_data import prepare_request_data
from utils.log import Log
from utils.util import generate_encryption_params

log = Log()


class UserClaimCouponService:
    def __init__(self, base_url, yaml_file_path=None):
        self.client = RequestHandler(base_url)
        if yaml_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.yaml_file_path = os.path.join(current_dir, "..", "..", "datas", "claim.yaml")
        else:
            self.yaml_file_path = yaml_file_path
        self.api_configs = self._load_api_configs()

    def _load_api_configs(self):
        """加载所有API配置"""
        try:
            with open(self.yaml_file_path, 'r', encoding='utf-8') as file:
                configs = list(yaml.safe_load_all(file))
            return configs
        except Exception as e:
            print(f"加载YAML配置失败: {e}")
            return []

    def _get_api_config(self, index):
        """根据索引获取API配置"""
        if 0 <= index < len(self.api_configs):
            return self.api_configs[index]
        return None

    def user_send_claim_sms(self):
        """发送领取验证码"""
        config = self._get_api_config(0)  # 第一个API配置
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_claim_coupon(self):
        """提交领取优惠券"""
        config = self._get_api_config(1)  # 第二个API配置
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_claim(self):
        """用户进行领取活动优惠券流程"""
        # 先发送验证码
        sms_result = self.user_send_claim_sms()
        # 使用更清晰的条件判断
        if sms_result and sms_result.status_code in [200, 400]:
            # 验证码发送成功后提交领取
            return self.user_claim_coupon()
        return sms_result
