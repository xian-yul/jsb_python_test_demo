class EnvConfig:
    """环境配置"""

    def __init__(self, env="test"):
        self.env = env
        self._validate_env()

    def _validate_env(self):
        """校验环境参数是否合法"""
        valid_envs = ["test", "preview"]
        if self.env not in valid_envs:
            raise ValueError(f"不支持的环境: {self.env}，支持的环境包括: {valid_envs}")

    @property
    def base_url(self):
        """根据环境返回基础域名"""
        config = {
            "test": {
                "OPERA_URL": "http://192.168.101.24:8050",
                "SELLER_URL": "http://192.168.101.24:8070",
                "USER_URL": "http://v3.www.jinsubao.test",
                "OPERA_PORT": "8050",
                "SELLER_PORT": "8070",
                "ERP_URL": "http://erp.jinsubao.test",
                "App_user_URL": "http://192.168.101.24:8095"
            },
            "preview": {
                "OPERA_URL": "https://admdm.jinsubao.cn",
                "SELLER_URL": "https://slrdm.jinsubao.cn",
                "USER_URL": "https://v3demo.jinsubao.cn",
                "ERP_URL": "https://erpdm.jinsubao.cn",
            },
        }
        return config.get(self.env, {})
