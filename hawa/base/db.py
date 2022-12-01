import MySQLdb
import mongoengine
from redis.client import StrictRedis

from hawa.base.decos import singleton
from hawa.config import project


@singleton
class DbUtil:
    _conn = None
    _cursor = None

    @property
    def conn(self):
        """link mysql by mysqlclient"""
        if project.COMPLETED:
            if not self._conn:
                self._conn = self.connect()
            return self._conn
        return self.connect()

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
        if not project.COMPLETED:
            return self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        if not self._cursor:
            self._cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
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
