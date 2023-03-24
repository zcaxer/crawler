# Welcome to Cursor



# 1. Try generating with command K on a new line. Ask for a pytorch script of a feedforward neural network
# 2. Then, select the outputted code and hit chat. Ask if there's a bug. Ask how to improve.
# 3. Try selecting some code and hitting edit. Ask the bot to add residual layers.
# 4. To try out cursor on your own projects, go to the file menu (top left) and open a folder.

# Nga_pymongo module

"""connect mongodb with motor and pymongo"""

#import asyncio
import motor.motor_asyncio
import pymongo

class Mongo:
    async_client=None
    sync_client=None

    def __init__(self):
        if self.async_client is None:
            self.async_client = motor.motor_asyncio.AsyncIOMotorClient()
        if self.sync_client is None:
            self.sync_client = pymongo.MongoClient(host='localhost', port=27017)

    async def write_to_db(self,json_data):
        bson_data=json_data
        self.async_client.replies.insert_one(bson_data)

    async def write_cookies_to_db(self,cookies):
        self.async_client.nga.info.insert_one({'cookies':cookies})

    def read_cookies(self):
        
        cookie=self.sync_client.nga.info.find_one({'cookies':{'$exists':True}})
        return cookie['cookies']
