# Nga_pymongo module

"""connect mongodb with motor and pymongo"""

#import asyncio
import motor.motor_asyncio

class Mongo:

    @classmethod
    def __init__(self):
        if self.client==None:
            self.client = motor.motor_asyncio.AsyncIOMotorClient()

    async def write_to_db(self,json_data):
        bson_data=json_data
        self.client.replies.insert_one(bson_data)

    async def write_cookies_to_db(self,cookies):
        self.client.nga.info.insert_one({'cookies':cookies})

    async def read_cookies(self):
        cookie=await self.client.nga.info.find_one({'cookies':{'$exists':True}})
        return cookie['cookies']