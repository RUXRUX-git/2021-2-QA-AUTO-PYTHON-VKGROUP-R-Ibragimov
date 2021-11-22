import pytest

from mysql.builder import MysqlBuilder


class Base:
    def prepare(self):
        pass

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, mysql_client):
        self.mysql_client = mysql_client
        self.mysql_builder = MysqlBuilder(self.mysql_client)

        self.prepare()
