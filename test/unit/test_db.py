import sys, logging, os
sys.path.append("../../src")
os.environ["HULU_ENV"] = "test"

import unittest, db
import mock

class TestDatabase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.redis = mock.Mock()
        self.client = db.Database(self.redis)

    def test_incr_vote_calls_redis_once(self):
        self.client.incrVote("test_key")
        self.redis.incr.assert_called_with("test_key")

    def test_when_redis_throws_exceptions_we_retry(self):
        self.redis.side_effect = [Exception("Redis Failed"), "test_value"]
        self.client.getVote("test_key")

    def test_when_redis_timesout_too_often_we_raise_exception(self):
        self.redis.side_effect = Exception("Redis Failed")
        self.client.getVote("test_key")

if __name__ == "__main__":
    unittest.main()
