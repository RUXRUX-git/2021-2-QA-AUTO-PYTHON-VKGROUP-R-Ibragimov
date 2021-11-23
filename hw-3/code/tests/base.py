import pytest


class TestBase:
    @pytest.fixture(scope="function", autouse=True)
    def login(self, api_client):
        api_client.post_login()
