import pytest

from mysql.client import MysqlClient

from constants import LOG_FILE_PATH


def pytest_addoption(parser):
    parser.addoption('--log_file_path', default=LOG_FILE_PATH)


@pytest.fixture()
def config(request):
    return {
        'log_file_path': request.config.getoption('--log_file_path')
    }


def pytest_configure(config):
    mysql_client = MysqlClient(user="root", password="pass", db_name="TEST_SQL", host="127.0.0.1", port=3306)
    if not hasattr(config, "workerinput"):
        mysql_client.recreate_db()

    mysql_client.connect()

    if not hasattr(config, "workerinput"):
        table_names = ["count_requests", "type_to_count", "most_popular_urls",
                       "top_sized_4xx_responses", "top_users_by_5xx_error"]
        for name in table_names:
            mysql_client.create_table(name)

    config.mysql_client = mysql_client


@pytest.fixture(scope="session")
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()
