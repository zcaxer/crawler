# Nga_pymongo module

"""connect mongodb with motor and pymongo"""

# import asyncio
from typing import Optional
import motor.motor_asyncio
import pymongo


class Mongo:
    _instance = None
    async_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
    sync_client: Optional[pymongo.MongoClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.async_client = motor.motor_asyncio.AsyncIOMotorClient()
            cls.sync_client = pymongo.MongoClient(host="localhost", port=27017)
        return cls._instance

    async def store_topic(self, topic):
        topic_id = str(topic.tid)
        if self.async_client is not None:
            client = self.async_client["nga_topic"][topic_id]
        for i in topic.posts:
            bson_data = i.to_dict()
            await client.insert_one(bson_data)
            query = {
                "pid": bson_data["pid"],
                "author_id": bson_data["author_id"],
                "date": bson_data["date"],
                "content": bson_data["content"],
                "reply_to": bson_data["reply_to"],
                "quote_to": bson_data["quote_to"],
            }
            result = await client.find_one(query)
            if result == None:
                await client.insert_one(bson_data)
        await self.async_client.nga.topics.update_one({"tid": topic.tid}, {"$set": topic.to_dict()}, upsert=True)

    def store_cookies(self, cookies):
        self.sync_client.nga.info.update_one({"cookies": {"$exists": True}}, {"$set": {"cookies": cookies}}, upsert=True)

    def read_cookies(self):
        cookie = self.sync_client.nga.info.find_one({"cookies": {"$exists": True}})
        return cookie["cookies"]

    async def search_posts_by_author_and_date(self, topic_id, author_id, date):
        topic_id = str(topic_id)
        if self.async_client is not None:
            client = self.async_client["nga_topic"][topic_id]
        query = {"author_id": author_id, "date": date}
        result = await client.find_one(query)
        if result == None:
            return None
        return result["pid"]

    async def get_crawler_info(self):
        self.async_client.nga.topics.find_all()

    async def get_page_count_and_last_post_date(self):
        """
        This function retrieves the page count and last post date from the nga.topics collection where status=1.
        """
        cursor = await self.async_client.nga.topics.find(
            {"status": 1}, {"_id": 0, "tid": 1, "page_count": 1, "last_post_date": 1,"title": 1,"last_post_pid": 1}
        )
        return cursor


if __name__ == "__main__":
    mongo = Mongo()
