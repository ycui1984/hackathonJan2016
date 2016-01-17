import sys, logging, os
sys.path.append("../../src")
os.environ["HULU_ENV"] = "test"

from webtest import TestApp
from app import app
import unittest, mock

class TestApplication(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.redis = mock.Mock()

        app.db_client = self.redis
        self.test_app = TestApp(app)

    def test_health_check(self):
        resp = self.test_app.get("/health_check")
        self.assertEqual(200, resp.status_int)

    def test_add_vote(self):
        self.test_app.get("/vote/test_key")

        self.redis.incrVote.assert_called_with(u"test_key")
        self.redis.getVote.assert_called_with(u"test_key")

    def test_get_vote(self):
        self.test_app.post("/clear", {"key":"test_key"})
        self.redis.clearVote.assert_called_with("test_key")

    @mock.patch('requests.get')
    def test_proxy_hulu(self, mock_requests):
        response = mock.Mock()
        response.status_code = 200
        mock_requests.return_value = response

        resp = self.test_app.get("/proxy_hulu")
        self.assertEqual(200, resp.status_int)
        mock_requests.assert_called_with("http://www.hulu.com")


if __name__ == "__main__":
    unittest.main()