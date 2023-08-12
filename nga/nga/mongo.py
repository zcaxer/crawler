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
            if i is not None:
                bson_data = i.to_dict()
                query = {
                    "index": bson_data["index"],
                    "author_id": bson_data["author_id"],
                    "date": bson_data["date"],
                    "content": bson_data["content"],
                    "reply_to": bson_data["reply_to"],
                    "quote_to": bson_data["quote_to"],
                }
                result = await client.find_one(query)
                if result == None:
                    await client.insert_one(bson_data)
        await self.async_client.nga.topics.update_one(
            {"tid": topic.tid}, {"$set": topic.to_dict()}, upsert=True
        )

    def store_cookies(self, cookies):
        self.sync_client.nga.info.update_one(
            {"cookies": {"$exists": True}}, {"$set": {"cookies": cookies}}, upsert=True
        )

    def read_cookies(self):
        cookie = self.sync_client.nga.info.find_one({"cookies": {"$exists": True}})
        return cookie["cookies"]

    async def search_post(self, topic_id, post_pid):
        """return post.index"""
        topic_id = str(topic_id)
        if self.async_client is not None:
            client = self.async_client["nga_topic"][topic_id]
        query = {"pid": post_pid}
        result = await client.find_one(query)
        if result == None:
            return None
        return result

    async def check_mongodb(self):
        try:
            await self.async_client.server_info()
            return True
        except Exception:
            return False
    

    async def get_topic_info(self):
        """
        This function retrieves  "status", "tid", "page_count", "last_post_date","title","last_post_index"
        """
        cursor = self.async_client.nga.topics.find(
            {"status": 1},
            {
                "_id": 0,
                "tid": 1,
                "page_count": 1,
                "last_post_date": 1,
                "title": 1,
                "last_post_index": 1,
                "anony_posters": 1,
                "new_titles": 1,
            },
        )
        docs=await cursor.to_list(length=None)
        return docs

    #delete a topic from mongodb
    async def delete_topic(self, tid):
        await self.async_client.nga.topics.delete_one({"tid": tid})
        await self.async_client.nga_topic[str(tid)].drop()

    def search_topic_by_title_str(self, topic_title_str):
        '''
        Searches for a topic by its title string using the NGA async client.
        Args:
            topic_title_str (str): The string to search for in the topic titles.
        Returns:
            int: The ID of the first topic whose title matches the given string.
        Raises:
        IndexError: If no topic is found or the search result is empty.
        '''
        topic=self.sync_client.nga.topics.find({"title": {"$regex": topic_title_str}})[0]
        return topic['tid'],topic['title']

if __name__ == "__main__":
    mongo = Mongo()
