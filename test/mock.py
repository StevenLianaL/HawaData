from hawa.base.db import MongoUtil
from hawa.config import project


def prepare_test():
    project.COMPLETED = True
    MongoUtil.connect()
