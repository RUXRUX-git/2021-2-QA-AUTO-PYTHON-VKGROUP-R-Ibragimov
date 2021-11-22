from models import CountRequests, \
    TypeToCount, \
    MostPopularUrls, \
    TopSized4xxRequests, \
    TopUsersBy5xxError


class MysqlBuilder:
    def __init__(self, client):
        self.client = client

    def creation_template(self, model, **kwargs):
        elem = model(**kwargs)
        self.client.session.add(elem)
        return elem

    def create_count_requests(self, count):
        return self.creation_template(CountRequests, count=count)

    def create_type_to_count(self, type, count):
        return self.creation_template(TypeToCount, type=type, count=count)

    def create_most_popular_urls(self, url, count):
        return self.creation_template(MostPopularUrls, url=url, count=count)

    def create_top_sized_4xx_requests(self, url, status_code, size, ip):
        return self.creation_template(TopSized4xxRequests, url=url, status_code=status_code, size=size, ip=ip)

    def create_top_users_by_5xx_error(self, ip, count):
        return self.creation_template(TopUsersBy5xxError, ip=ip, count=count)
