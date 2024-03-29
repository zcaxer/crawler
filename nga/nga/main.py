import re
import os
import traceback
import logging
from datetime import datetime
import shutil

from bs4 import BeautifulSoup as bs

from .request import Request
from .mongo import Mongo
from .nga import Nga
from .parser import Parser as parser

# TODO:重构，充分利用异步
# TODO:find post I interested in


class Nga_clawler:
    mongo = None
    pattern=None

    def __init__(self):
        self.request = Request()
        if Nga_clawler.mongo is None:
            Nga_clawler.mongo = Mongo()

    def __del__(self):
        cookie_jar = self.request.session.cookie_jar
        cookies = {cookie.key: cookie.value for cookie in cookie_jar}
        self.mongo.store_cookies(cookies)
        # self.request.session.close()
        self.mongo.async_client.close()
        self.mongo.sync_client.close()

    async def update_one(self, topic):
        pass

    async def update_all(self,finished=False):
        topics = await self.mongo.get_topic_info(finished)
        for topic_dict in topics:
            topic = Nga.Topic(
                topic_dict["tid"],
                topic_dict["page_count"],
                topic_dict["last_post_date"],
                topic_dict["last_post_index"],
            )
            topic.anony_posters = topic_dict["anony_posters"]

            try:
                html, alredy_exits = await self.request.get_page(
                    topic.tid, topic.page_count
                )
                soup = bs(html, "lxml")
                page_title = soup.title.text
                if page_title in ("找不到主题", "帖子发布或回复时间超过限制", "帖子被设为隐藏", "帖子审核未通过", "帐号权限不足"):
                    await self.mongo.async_client.nga.topics.update_one(
                        {"tid": topic.tid}, {"$set": {"status": 2}}
                    )
                    logging.info("id:%d finished,%s", topic.tid,page_title)
                    continue
                if page_title == "帖子正等待审核":
                    continue
                topic.title = await parser.get_title(soup)
                if not topic.title == topic_dict["title"]:
                    if 'new_titles' in topic_dict.keys():
                        topic.new_titles = topic_dict['new_titles']
                    else:
                        topic.new_titles = []
                    topic.new_titles.append(topic.title)
                    topic.title = topic_dict['title']  # 帖子改名

                s_posttime = soup.find_all("div", {"class": "postInfo"})
                last_posttime = s_posttime[-1].text
                last_post_date = datetime.strptime(
                    last_posttime, "%Y-%m-%d %H:%M")
                if last_post_date != topic.last_post_date:
                    logging.info("%s发现更新", topic.title)
                    old_last_post_index = topic.last_post_index
                    max_page = await parser.get_page_count(soup)
                    # nga_clawler = Nga_clawler(id)
                    for page_number in range(topic.page_count, max_page + 1):
                        if not page_number == topic.page_count:
                            html, alredy_exits = await self.request.get_page(
                                topic.tid, page_number, topic.title
                            )
                            soup = bs(html, "lxml")
                        if not alredy_exits:
                            self.store_html(topic.title, html, page_number)
                        topic.result_html += await parser.page_parser(self.request,
                                                                      soup, page_number, topic
                                                                      )
                    with open(
                        f"results/{topic.title}.html", "r", encoding="utf-8"
                    ) as r:
                        old_lines = r.readlines()[7:-2]
                        new_lines = topic.result_html.splitlines()
                        pattern = re.compile(
                            r"\s*\<\s*p\s*\>\s*(\d+)\s*:.*\<\s*/p\s*\>\s*"
                        )
                        while True:
                            n = int(pattern.match(new_lines[0]).group(1))
                            if n <= old_last_post_index:
                                new_lines.pop(0)
                            else:
                                break
                        topic.result_html = ""
                        for line in old_lines:
                            topic.result_html = topic.result_html + line
                        for line in new_lines:
                            topic.result_html = topic.result_html + line + "\n"
                    topic.page_count = max_page
                    topic.write_to_result_html()
                    await self.mongo.store_topic(topic)
            except Exception as e:
                traceback.print_exc()
                logging.info("%d请求失败,%s", topic.tid,page_title)

    @staticmethod
    def store_html(title, html, page_number, result=False):
        if result:
            pass
        else:
            with open(f"htmls/{title}/{title}{page_number}.html", "w", encoding="gbk") as f:
                f.write(html)
            logging.info("写入%s%d.html", title, page_number)

    async def start(self, topic, refresh_old_html=False):
        page1, need_write = await self.request.get_page(
            topic.tid, 1, topic_title=topic.title
        )
        soup = bs(page1, "lxml")
        topic.title = await parser.get_title(soup)
        topic.page_count = await parser.get_page_count(soup)
        if not os.path.exists(f"htmls/{topic.title}"):
            logging.info("创建文件夹%s", topic.title)
            os.mkdir(f"htmls/{topic.title}")
        if need_write:
            self.store_html(topic.title, page1, 1)
        logging.info("开始解析%s第1页", topic.title)
        topic.result_html += await parser.page_parser(self.request, soup, 1, topic)
        for page_number in range(2, topic.page_count + 1):
            logging.info("开始请求%s%d.html", topic.title, page_number)
            html, need_write = await self.request.get_page(
                topic.tid, page_number, topic.title, refresh_old_html
            )
            if need_write:
                self.store_html(topic.title, html, page_number)
            if not html == "" and html is not None:
                logging.info("开始解析%s第%d页", topic.title, page_number)
                soup = bs(html, "lxml")
                topic.result_html += await parser.page_parser(self.request, soup, page_number, topic)
        topic.write_to_result_html()
        topic.status = Nga.TopicStatus.LIVE
        await self.mongo.store_topic(topic)

    async def delete_topic(self, title_str):
        tid, title = self.mongo.search_topic_by_title_str(title_str)
        await self.mongo.delete_topic(tid)
        os.remove(f'results/{title}.html')
        shutil.rmtree(f'htmls/{title}')

    async def get_index(self):
        r = await self.request.session.get(Nga.url_index)
        content =await r.text()
        content = content.replace("�", "")
        with open("index.html", "w") as f:
            f.write(content)
        soup = bs(content, "lxml")
        topic_tags = soup.find_all("a", {"class": "topic"})
        replies_tags = soup.find_all("a", {"class": "replies"})

        if Nga_clawler.pattern==None:
            Nga_clawler.pattern=re.compile(r"(\d+)")

        topic_list=[]
        for topic_tag in topic_tags:
            topic_id=Nga_clawler.pattern.search(topic_tag["href"]).group(1)
            topic_title=topic_tag.text
            topic_replies=int(replies_tags[int(topic_id)-1].text)
            topic=Nga.Topic(topic_id)
            topic_list.append(topic)


        print(topic_tags[-1]["href"], topic_tags[-1].text)
        print(replies_tags[-1].text)
