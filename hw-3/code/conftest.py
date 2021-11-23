import pytest

import utils


@pytest.fixture(scope="function")
def api_client():
    return utils.create_api_client()


@pytest.fixture(scope="function")
def random_name():
    return utils.create_random_name()
