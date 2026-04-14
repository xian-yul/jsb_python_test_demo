import requests
import json

from config.header_builder import HeaderBuilder
from utils.log import Log

log = Log()


class RequestHandler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _log_request(self, method, url, **kwargs):
        """日志记录"""
        log.info(f"【Request】{method.upper()} {url}")
        if kwargs.get("headers"):
            log.debug(f"Headers: {kwargs['headers']}")
        if kwargs.get("json"):
            log.debug(f"Body: {json.dumps(kwargs['json'], ensure_ascii=False)}")

    def request(self, method, endpoint, **kwargs):
        """统一请求入口"""
        url = self.base_url + endpoint
        headers = kwargs.pop("headers", {})

        # 自动追加基础header
        base_headers = HeaderBuilder.get_base_headers()
        headers = {**base_headers, **headers}  # 允许覆盖

        self._log_request(method, url, headers=headers, **kwargs)

        try:
            response = self.session.request(method, url, headers=headers, **kwargs)
            log.info(f"【Response】status: {response.status_code}")
            log.debug(f"content: {response.text[:500]}")  # 避免日志爆炸
            return response
        except Exception as e:
            log.error(f"Request failed: {str(e)}")
            raise

    # 快捷方法
    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, json_data=None, **kwargs):
        return self.request("POST", endpoint, json=json_data, **kwargs)

    def put(self, endpoint, json_data=None, **kwargs):
        return self.request("PUT", endpoint, json=json_data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
