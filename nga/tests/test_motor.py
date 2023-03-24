import sys
sys.path.append("..")
from nga.mongo import Mongo
import json
import asyncio

#import nga.async_mongo as am
#from nga.request_handler import get_session

#am.get_client()


def get_json():
    with open('../nga/nga.json', 'r', encoding='utf-8') as f:
        config_json = json.load(f)
        return config_json

async def add_cookie():
    cookie=get_json()['cookies']
    client=mongo.async_client
    client.nga.info.insert_one({'cookies':cookie})




if __name__ == '__main__':
    mongo=Mongo()
  #  cookies = asyncio.run(mongo.read_cookies())
    cookies=mongo.read_cookies()
    print(cookies)
