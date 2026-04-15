import os

from dotenv import load_dotenv

from config.request_handler import RequestHandler
from config.request_data import prepare_request_data
from utils.get_yaml import load_api_yaml, get_config_by_index, get_config_by_field
from utils.log import Log
from utils.util import  get_latest_token, save_user_token

log = Log()
load_dotenv('E:\\jsb_python_test_demo\\get_token.env')


class RegularFunctionsCase:
    def __init__(self, base_url, yaml_file_path=None):
        self.client = RequestHandler(base_url)
        if yaml_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.yaml_file_path = os.path.join(current_dir, "..", "..", "datas", "regular.yaml")
        else:
            self.yaml_file_path = yaml_file_path
        self.api_configs = self._load_api_configs()

    def _load_api_configs(self):
        """加载所有API配置"""
        return load_api_yaml(self.yaml_file_path)

    def _get_api_config(self, index):
        """根据索引获取API配置"""
        return get_config_by_index(self.api_configs, index)

    def _get_api_config_by_field(self, field_name, field_value):
        """根据字段名和值获取API配置"""
        return get_config_by_field(self.api_configs, field_name, field_value)

    # 使用示例
    """
    config = self._get_api_config_by_field('name', '用户登录')  # 根据接口名称获取
    config = self._get_api_config_by_field('url', '/api/login')  # 根据URL获取
    """

    def user_set_password(self):
        """设置账号密码"""
        config = self._get_api_config_by_field('API_NAME', '买家设置密码')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        jsb_token = os.getenv('USER_AUTH_TOKEN')
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def password_login(self):
        """进行密码登录"""
        # config = self._get_api_config(1)  # 第二个API配置
        config = self._get_api_config_by_field('API_NAME', '买家密码登录')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        try:
            login_result = self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                               headers=request_data['headers'])
            if login_result and login_result.status_code == 200:
                save_user_token(login_result)
                log.info(f"登录成功: {request_data['name']}")
            else:
                log.warning(
                    f"登录失败: {request_data['name']}, 状态码: {login_result.status_code if login_result else 'None'}")
            return login_result
        except Exception as e:
            log.error(f"登录请求异常: {request_data['name']}, 错误信息: {str(e)}")
            return None

    def reset_password(self):
        """重置密码"""
        config = self._get_api_config_by_field('API_NAME', '买家重置密码')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def get_setting(self):
        """获取账户安全信息"""
        config = self._get_api_config_by_field('API_NAME', '获取账号安全设置信息')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        print(jsb_token)
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_phone_sms(self):
        extra_body = {'smsType': '2', 'phone': '17200000005'}
        return self.phone_sms(extra_body)

    def phone_sms(self, extra_body=None):
        """进行手机号登录 - 发送验证码"""
        config = self._get_api_config_by_field('API_NAME', '手机号登录 - 发送验证码')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config, extra_body=extra_body)
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def phone_login(self):
        """进行手机号登录"""
        config = self._get_api_config_by_field('API_NAME', '手机号登录')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def upd_old_phone(self):
        """修改手机号"""
        config = self._get_api_config_by_field('API_NAME', '修改手机号 - 旧手机号校验')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def upd_new_phone(self):
        """修改手机号"""
        config = self._get_api_config_by_field('API_NAME', '修改手机号 - 新手机号校验')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_upd_old_phone_sms(self):
        """进行旧手机号登录 - 发送验证码"""
        extra_body = {'smsType': '8', 'phone': '17200000003'}
        return self.phone_sms(extra_body)

    def user_upd_new_phone_sms(self):
        """进行新手机号登录 - 发送验证码"""
        extra_body = {'smsType': '8', 'phone': '17200000003'}
        return self.phone_sms(extra_body)

    def user_manual_appeal(self):
        """人工申诉"""
        config = self._get_api_config_by_field('API_NAME', '人工申诉提交')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_invite_code(self):
        """验证企业邀请码"""
        config = self._get_api_config_by_field('API_NAME', '验证企业邀请码')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_auth_org(self):
        """验证身份加入企业"""
        config = self._get_api_config_by_field('API_NAME', '验证身份 - 加入企业')  # 根据接口名称获取
        if not config:
            return None
        extra_body = {'smsType': '9'}
        request_data = prepare_request_data(config, extra_body=extra_body)
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_upd_password(self):
        """修改密码"""
        config = self._get_api_config_by_field('API_NAME', '修改密码')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        jsb_token = get_latest_token()
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def user_auth_org_sms(self):
        """进行旧手机号登录 - 发送验证码"""
        extra_body = {'phone': '17200000003'}
        return self.phone_sms(extra_body)

    def opera_login_sms(self):
        """运营端发送验证码"""
        extra_body = {'phone': '13600136002'}
        return self.phone_sms(extra_body)

    def opera_phone_login(self):
        """运营端手机号登录"""
        config = self._get_api_config_by_field('API_NAME', '运营端登录')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def opera_reset_user_password(self):
        """重置用户手机号"""
        config = self._get_api_config_by_field('API_NAME', '重置密码')  # 根据接口名称获取
        if not config:
            return None
        request_data = prepare_request_data(config)
        jsb_token = get_latest_token('opera')
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])


    def opera_reset_user_password(self):
        """重置用户手机号"""
        config = self._get_api_config_by_field('API_NAME', '重置密码')
        if not config:
            return None
        request_data = prepare_request_data(config)
        jsb_token = get_latest_token('opera')
        headers = request_data['headers']
        headers['Authorization'] = jsb_token
        log.info(f"执行: {request_data['name']}")
        return self.client.request(request_data['method'], request_data['url'], json=request_data['data'],
                                   headers=request_data['headers'])

    def execute_api_with_custom_data(self, api_name: str, custom_body: dict):
        """
        使用自定义数据执行API

        Args:
            api_name: API名称
            custom_body: 自定义请求体数据

        Returns:
            响应对象
        """
        config = self._get_api_config_by_field('API_NAME', api_name)
        if not config:
            log.error(f"未找到API配置: {api_name}")
            return None

        request_data = prepare_request_data(config, extra_body=custom_body)
        log.info(f"执行: {request_data['name']}, 数据: {custom_body}")

        return self.client.request(
            request_data['method'],
            request_data['url'],
            json=request_data['data'],
            headers=request_data['headers']
        )

