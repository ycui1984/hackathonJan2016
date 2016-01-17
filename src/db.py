import redis
import config
import logging

logger = logging.getLogger(__name__)


class Database():
    def __init__(self, client, retries=3):
        self.client = client
        self.retries = retries

    def getVote(self, key):
        for i in range(self.retries):
            try:
                return self.client.get(key)
            except Exception as ex:
                if i == self.retries - 1:
                    logger.exception(ex)
                    raise

    def incrVote(self, key):
        self.client.incr(key)

    def clearVote(self, key):
        self.client.delete(key)


def get_basic_client(socket_timeout=.2):
    r_client = redis.StrictRedis.from_url(config.REDIS_URL, socket_timeout=socket_timeout)
    return Database(r_client)
