# utils/api_client.py
import requests


class APIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, endpoint, params=None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params)

    def post(self, endpoint, data=None, json=None):
        return self.session.post(f"{self.base_url}{endpoint}", data=data, json=json)

    def put(self, endpoint, data=None, json=None):
        return self.session.put(f"{self.base_url}{endpoint}", data=data, json=json)

    def delete(self, endpoint, params=None):
        return self.session.delete(f"{self.base_url}{endpoint}", params=params)
