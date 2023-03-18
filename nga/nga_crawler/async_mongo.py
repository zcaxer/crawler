# Nga_pymongo module

"""connect mongodb with motor and pymongo"""

import asyncio
import traceback
#import pymongo
import motor.motor_asyncio

def get_client():
#client=motor.MotorClient.open_sync()
    client=motor.motor_asyncio.AsyncIOMotorClient()
    return client

client=get_client()
db_replies=client.nga_replies

async def get_server_info():
    try:
        print(await client.server_info())
    except ConnectionError :
        traceback.print_exc()
        print('connect failed')

async def write_to_db(bson):
    db_replies.insertOne(bson)

if __name__=='__main__':

    loop=asyncio.get_event_loop()
    loop.run_until_complete(get_server_info())
