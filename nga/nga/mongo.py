#import asyncio
import motor.motor_asyncio
import pymongo


class Mongo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.async_client = motor.motor_asyncio.AsyncIOMotorClient()
            cls._instance.sync_client = pymongo.MongoClient(
                host='localhost', port=27017)
        return cls._instance

    async def write_to_db(self, json_data):
        bson_data = json_data
        await self.async_client.replies.insert_one(bson_data)

    async def write_cookies_to_db(self, cookies):
        await self.async_client.nga.info.insert_one({'cookies': cookies})

    def read_cookies(self):

        cookie = self.sync_client.nga.info.find_one(
            {'cookies': {'$exists': True}})
        return cookie['cookies']
