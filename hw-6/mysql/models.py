from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CountRequests(Base):
    __tablename__ = "count_requests"
    __table_args__ = {"mysql_charset": "utf8"}

    def __repr__(self):
        return f"<CountRequests(id='{self.id}', count='{self.count}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)


class TypeToCount(Base):
    __tablename__ = "type_to_count"
    __table_args__ = {"mysql_charset": "utf8"}

    def __repr__(self):
        return f"<TypeToCount(id='{self.id}', type='{self.type}', count='{self.count}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)


class MostPopularUrls(Base):
    __tablename__ = "most_popular_urls"
    __table_args__ = {"mysql_charset": "utf8"}

    def __repr__(self):
        return f"<MostPopularUrls(id='{self.id}', url='{self.url}', count='{self.count}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(400), nullable=False)
    count = Column(Integer, nullable=False)


class TopSized4xxRequests(Base):
    __tablename__ = "top_sized_4xx_responses"
    __table_args__ = {"mysql_charset": "utf8"}

    def __repr__(self):
        return f"<TopSized4xxRequests(" \
               f"id='{self.id}', " \
               f"url='{self.url}', " \
               f"status_code='{self.status_code}', " \
               f"size='{self.size}', " \
               f"ip='{self.ip}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(400), nullable=False)
    status_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(String(50), nullable=False)


class TopUsersBy5xxError(Base):
    __tablename__ = "top_users_by_5xx_error"
    __table_args__ = {"mysql_charset": "utf8"}

    def __repr__(self):
        return f"<TopUsersBy5xxError(" \
               f"id='{self.id}', " \
               f"ip='{self.ip}', " \
               f"count='{self.count}')>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)
