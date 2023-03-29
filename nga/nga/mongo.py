# Nga_pymongo module

"""connect mongodb with motor and pymongo"""

#import asyncio
from typing import Optional
import motor.motor_asyncio
import pymongo


class Mongo:
    _instance=None
    async_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
    sync_client: Optional[pymongo.MongoClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.async_client = motor.motor_asyncio.AsyncIOMotorClient()
            cls.sync_client = pymongo.MongoClient(host='localhost', port=27017)
        return cls._instance

    async def write_posts_to_db(self,topic):
        client=self.async_client['nga_topic'][topic.title]
        for i in topic.posts:
            bson_data = i.to_dict()
            await client.insert_one(bson_data)

    async def write_cookies_to_db(self, cookies):
        await self.async_client.nga.info.insert_one({'cookies': cookies})

    def read_cookies(self):

        cookie = self.sync_client.nga.info.find_one(
            {'cookies': {'$exists': True}})
        return cookie['cookies']
