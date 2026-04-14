class HeaderBuilder:
    @staticmethod
    def get_base_headers():
        """基础公共头"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Automation-Test-Framework"
        }

    @staticmethod
    def get_auth_headers(token=None):
        """带认证的请求头"""
        headers = HeaderBuilder.get_base_headers()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def get_multipart_headers(token=None):
        """文件上传专用头"""
        headers = HeaderBuilder.get_auth_headers(token)
        # 移除Content-Type，requests库会自动设置boundary
        headers.pop("Content-Type", None)
        return headers
