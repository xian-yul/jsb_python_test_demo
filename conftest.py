import pytest
import logging
import allure
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ========== 你现有的代码（保留）==========

@pytest.fixture(autouse=True)
def setup_test_env(request):
    test_name = request.node.name
    logging.info(f"Setting up test environment for {test_name}")
    print(f"Setting up test environment for {test_name}", flush=True)
    yield
    print(f"Tearing down test environment for {test_name}", flush=True)
    logging.info(f"Tearing down test environment for {test_name}")


@pytest.fixture(scope="session", autouse=True)
def setup_allure_environment():
    """写入 environment.properties，供 allure 报告读取"""
    allure_dir = "output/allure-results"
    os.makedirs(allure_dir, exist_ok=True)
    env_file = os.path.join(allure_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write("app=金塑宝\nversion=1.0\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        allure.attach("失败详情", str(report.longrepr), allure.attachment_type.TEXT)


# ========== 新增：全局重跑 + 网络重试 ==========

def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.get_closest_marker("flaky"):
            continue
        item.add_marker(
            pytest.mark.flaky(
                reruns=2,
                reruns_delay=1,
                only_rerun=[
                    "requests.exceptions.Timeout",
                    "requests.exceptions.ConnectionError",
                    "requests.exceptions.ChunkedEncodingError",
                    "urllib3.exceptions.ProtocolError",
                ]
            )
        )


@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504, 429],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    _original = session.request

    def _request(method, url, **kwargs):
        kwargs.setdefault("timeout", 10)
        return _original(method, url, **kwargs)

    session.request = _request

    return session