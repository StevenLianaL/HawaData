import MySQLdb
import mongoengine
import sqlalchemy
from redis.client import StrictRedis

from hawa.base.decos import singleton
from hawa.config import project

metadata = sqlalchemy.MetaData()


@singleton
class DbUtil:
    _conn = None
    _cursor = None

    @property
    def conn(self):
        if project.COMPLETED:
            if not self._conn:
                self._conn = self.db_engine
            return self._conn
        return self.db_engine

    @property
    def db_engine(self):
        database_url = f"{project.DB_MODE}://{project.DB_USER}:{project.DB_PSWD}@{project.DB_HOST}/" \
                       f"{project.DB_NAME}?charset=utf8"
        engine = sqlalchemy.create_engine(database_url, encoding='utf-8')
        return engine

    def connect(self):
        return MySQLdb.connect(
            host=project.DB_HOST,
            port=project.DB_PORT,
            user=project.DB_USER,
            passwd=project.DB_PSWD,
            db=project.DB_NAME,
        )

    @property
    def cursor(self):
        if not self._cursor:
            conn = self.connect()
            self._cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        return self._cursor


class MongoUtil:
    @classmethod
    def connect(self):
        mongoengine.connect(
            project.MONGO_DB,
            host=project.MONGO_HOST, port=project.MONGO_PORT,
            username=project.MONGO_USER,
            password=project.MONGO_PSWD,
            authentication_source=project.MONGO_AUTH_DB
        )


@singleton
class RedisUtil:
    @property
    def conn(self):
        return StrictRedis(
            host=project.REDIS_HOST,
            db=project.REDIS_DB,
            decode_responses=True,
        )
