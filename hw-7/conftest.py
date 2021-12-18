import pytest

from mock import flask_mock
from config import MOCK_HOST, MOCK_PORT
from client.socket_client import SocketClient
import utils
import warnings


@pytest.fixture(scope='session')
def socket_client():
    return SocketClient(MOCK_HOST, MOCK_PORT)


@pytest.fixture(scope='function')
def random_user():
    return utils.create_random_user()


@pytest.fixture(scope='function')
def random_first_name():
    return utils.create_random_first_name()


@pytest.fixture(scope='function')
def random_last_name():
    return utils.create_random_last_name()


def pytest_configure(config):
    flask_mock.run_mock()


def pytest_unconfigure(config):
    # Отлавливаем ворнинги и игнорируем их, поскольку UserWarning по поводу того, что функция
    # environ['werkzeug.server.shutdown'] является устаревшей, вызывается в момент вызова метода
    # shutdown() у сервера
    # P.S. Логи из всех щелей лезут, ужас
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        SocketClient(MOCK_HOST, MOCK_PORT).get('/shutdown')
