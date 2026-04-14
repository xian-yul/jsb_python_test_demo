import pytest
import logging

@pytest.fixture(autouse=True)
def setup_test_env(request):
    """自动使用的fixture，每个测试都会执行"""
    test_name = request.node.name
    logging.info(f"Setting up test environment for {test_name}")
    print(f"Setting up test environment for {test_name}", flush=True)
    yield
    print(f"Tearing down test environment for {test_name}", flush=True)
    logging.info(f"Tearing down test environment for {test_name}")
