import pytest

@pytest.fixture(autouse=True)
def setup_test_env(request):
    """自动使用的fixture，每个测试都会执行"""
    test_name = request.node.name
    print(f"Setting up test environment for {test_name}")
    yield
    print(f"Tearing down test environment for {test_name}")
