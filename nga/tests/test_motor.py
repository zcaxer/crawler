import unittest
import sys
sys.path.append('..')
from nga.mongo import Mongo


class TestMongo(unittest.TestCase):
    def setUp(self):
        self.mongo = Mongo()

    def test_read_cookies(self):
        cookies = {'key': 'value'}
        self.mongo.write_cookies_to_db(cookies)
        result = self.mongo.read_cookies()
        self.assertEqual(result, cookies)


if __name__ == '__main__':
    unittest.main()
