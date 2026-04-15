import allure

from utils.util import save_user_token, save_opera_token


class RegularFunctionsImplement:
    def __init__(self, regular_functions_case):
        self.regular = regular_functions_case

    def user_phone_login(self):
        """用户进行手机号登录流程"""
        # 先发送验证码
        sms_result = self.regular.user_phone_sms()
        allure.attach("先发送验证码")
        # 使用更清晰的条件判断
        if sms_result.status_code in [200, 400]:
            allure.attach("验证码发送成功后进行登录操作")
            # 验证码发送成功后进行登录操作
            login_result = self.regular.phone_login()
            # 登录成功后保存token
            if login_result and login_result.status_code == 200:
                save_user_token(login_result)
            return login_result
        return sms_result

    def opera_login(self):
        """用户进行手机号登录流程"""
        # 先发送验证码
        sms_result = self.regular.opera_login_sms()
        allure.attach("先发送验证码")
        # 使用更清晰的条件判断
        if sms_result and sms_result.status_code in [200, 400]:
            allure.attach("验证码发送成功后进行登录操作")
            # 验证码发送成功后进行登录操作
            login_result = self.regular.opera_phone_login()
            # 登录成功后保存token
            if login_result and login_result.status_code == 200:
                save_opera_token(login_result)
            return login_result
        return sms_result

    def user_password_login(self):
        """用户进设置密码并登录流程"""
        # 先设置密码
        password_set_result = self.regular.user_set_password()
        # 使用更清晰的条件判断
        if password_set_result and password_set_result.status_code in [200, 400]:
            login_result = self.regular.phone_login()
            # 登录成功后保存token
            if login_result and login_result.status_code == 200:
                save_user_token(login_result)
            return login_result
        return password_set_result

    def user_reset_password(self):
        """
       重置账号密码
       1.先进行手机号登录
       2.进行重置密码
       """
        self.user_phone_login()
        return self.regular.reset_password()

    def upd_user_phone(self):
        """
        修改手机号操作
        1.先进行手机号登录
        2.旧手机号短信验证
        3.修改手机号
        4.新手机号短信验证
        """
        self.user_phone_login()
        self.regular.user_upd_old_phone_sms()
        self.regular.upd_old_phone()
        self.regular.user_upd_new_phone_sms()
        return self.regular.upd_new_phone()

    def user_butler_certification(self):
        """
        E管家加入企业
        1.手机号登录
        2.验证企业邀请码
        3.验证手机号
        4.加入企业
        """
        self.user_phone_login()
        self.regular.user_auth_org_sms()
        return self.regular.user_auth_org()

    def get_user_setting(self):
        """
        获取用户账户安全信息
        1.先进行手机号登录
        2.获取账户安全信息
        3.验证身份 加入企业
        """
        self.user_phone_login()
        # self.regular.user_auth_org_sms()
        return self.regular.get_setting()

    def user_update_password(self):
        """
         用户修改密码
         1.先进行手机号登录
         2.修改手机密码
        """
        self.user_phone_login()
        return self.regular.user_upd_password()

    def verify_invite_code(self):
        self.user_phone_login()
        return self.regular.user_invite_code()

    def opera_reset_user(self):
        """
           重置用户密码
           1.先进行手机号登录运营
           2.进行重置用户密码
        """
        self.opera_login()
        return self.regular.opera_reset_user_password()
