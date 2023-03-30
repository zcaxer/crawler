import sys
sys.path.append('..')
from nga.mongo import Mongo

mongo = Mongo()

def test_read_cookies():
    result = mongo.read_cookies()
    print(result)


if __name__ == '__main__':
    test_read_cookies()
