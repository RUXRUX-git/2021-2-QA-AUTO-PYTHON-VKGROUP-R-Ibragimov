from utils import count_requests, type_to_count, url_to_count, size_to_4xx_response, ip_with_5xx_response_to_count
from tests.base_mysql import Base
from mysql.models import CountRequests, TypeToCount, MostPopularUrls, TopSized4xxRequests, TopUsersBy5xxError


# Захотелось сделать явное переопределение метода, нагуглил такое решение
def overrides(interface_class):
    def overrider(method):
        assert (method.__name__ in dir(interface_class))
        return method

    return overrider


class TestCountRequests(Base):
    @overrides(Base)
    def prepare(self, config):
        req_count = count_requests(config['log_file_path'])
        self.mysql_builder.create_count_requests(req_count)
        self.expected_len = 1

    def test_count_requests(self):
        req_count = self.mysql_client.session.query(CountRequests).all()
        assert len(req_count) == self.expected_len


class TestTypeToCount(Base):
    @overrides(Base)
    def prepare(self, config):
        req_type_to_count = type_to_count(config['log_file_path'])
        for elem in req_type_to_count:
            self.mysql_builder.create_type_to_count(elem["value"], elem["count"])
        self.expected_len = len(req_type_to_count)

    def test_type_to_count(self):
        req_type_to_count = self.mysql_client.session.query(TypeToCount).all()
        assert len(req_type_to_count) == self.expected_len


class TestMostPopularUrls(Base):
    @overrides(Base)
    def prepare(self, config):
        most_popular_urls = url_to_count(config['log_file_path'])
        for elem in most_popular_urls:
            self.mysql_builder.create_most_popular_urls(elem["value"], elem["count"])
        self.expected_len = len(most_popular_urls)

    def test_most_popular_urls(self):
        most_popular_urls = self.mysql_client.session.query(MostPopularUrls).all()
        assert len(most_popular_urls) == self.expected_len


class TestTopSized4xxRequests(Base):
    @overrides(Base)
    def prepare(self, config):
        top_sized_requests = size_to_4xx_response(config['log_file_path'])
        for elem in top_sized_requests:
            self.mysql_builder.create_top_sized_4xx_requests(
                url=elem["url"],
                status_code=elem["status_code"],
                size=elem["size"],
                ip=elem["ip"]
            )
        self.expected_len = len(top_sized_requests)

    def test_top_sized_requests(self):
        top_sized_requests = self.mysql_client.session.query(TopSized4xxRequests).all()
        assert len(top_sized_requests) == self.expected_len


class TestTopUsersBy5xxError(Base):
    @overrides(Base)
    def prepare(self, config):
        top_users_by_error = ip_with_5xx_response_to_count(config['log_file_path'])
        for elem in top_users_by_error:
            self.mysql_builder.create_top_users_by_5xx_error(
                ip=elem["ip"], count=elem["count"]
            )
        self.expected_len = len(top_users_by_error)

    def test_top_users_by_error(self):
        top_users_by_error = self.mysql_client.session.query(TopUsersBy5xxError).all()
        assert len(top_users_by_error) == self.expected_len
