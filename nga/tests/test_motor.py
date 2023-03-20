import sys
sys.path.append("..")
from nga.async_mongo import get_client
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
    
    client=get_client()
    client.nga.info.insert_one({'cookies':cookie})


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_cookie())
