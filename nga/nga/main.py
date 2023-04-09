import re
import os
import traceback
import argparse
import asyncio
import logging
from datetime import datetime
from bs4 import BeautifulSoup as bs
import aiofiles

from .request import Request
from .mongo import Mongo
from .nga import Nga
from .parser import Parser as parser

# TODO:查找回复内容原文并展示
# TODO:重构，单元化
# TODO:update posts
# TODO:find post I interested in


class Nga_clawler:
    request = None
    mongo = None
    topics = []

    def __init__(self, topic_id_list=[]):
        if self.request is None:
            self.request = Request()
        if Nga_clawler.mongo is None:
            Nga_clawler.mongo = Mongo()
        for i in topic_id_list:
            self.topics.append(Nga.Topic(i))

    def __del__(self):
        cookie_jar = self.request.session.cookie_jar
        cookies = {cookie.key: cookie.value for cookie in cookie_jar}
        self.mongo.store_cookies(cookies)
        # self.request.session.close()
        self.mongo.async_client.close()
        self.mongo.sync_client.close()

    async def update(self):
        topics =  await self.mongo.get_topic_info()
        for topic_dict in topics:
            topic = Nga.Topic(
                topic_dict['tid'], topic_dict['page_count'], topic_dict['last_post_date'])
            try:
                rsps = await self.request.get_page(topic.tid, topic.page_count)
                soup = bs(rsps.text, 'lxml')
                t = soup.title.text
                title = await parser.get_title(soup)
                if t in ('找不到主题', '帖子发布或回复时间超过限制', '帖子被设为隐藏', '帖子审核未通过'):
                    await self.mongo.async_client.nga.topics.update_one({"tid": topic.tid}, {"$set": {"status": 2}})
                    logging.info('id:%d finished', topic.tid)
                elif t == "帖子正等待审核":
                    break
                elif not title == topic_dict['title']:
                    topic.title = title
                    pass  # 帖子改名
                else:
                    s_posttime = soup.find_all('div', {'class': 'postInfo'})
                    last_posttime = s_posttime[-1].text
                    last_post_date = datetime.strptime(
                        last_posttime, '%Y-%m-%d %H:%M')
                    if last_post_date != topic.last_post_date:
                        max_page = await parser.get_page_count(soup)
                        #nga_clawler = Nga_clawler(id)
                        for p in range(topic.page_count, max_page+1):
                            if p == topic.page_count:
                                html = rsps
                            else:
                                html = self.request.get_page(
                                    topic.tid, p, topic.title)
                            with open(f'htmls/{topic.title}/{topic.title}{p}.html', 'w', encoding="gbk") as f:
                                f.write(html)
                                logging.info('写入%s%d.html', topic.title, p)
                            topic.result_html += parser.page_parser(
                                soup, p, topic)

                        with open(f'results/{topic.title}.html', "r", encoding='utf-8') as r:
                            old_lines = r.readlines()[7:-2]
                            new_lines = topic.result_html.splitlines()
                            pattern = re.compile(
                                r'\s*\<\s*p\s*\>\s*(\d+)\s*:.*\<\s*/p\s*\>\s*')
                            while True:
                                n = int(pattern.match(new_lines[0]).group(1))
                                if n <= topic.last_post_index:
                                    new_lines.pop(0)
                                else:
                                    break
                            topic.result_html = ''
                            for line in old_lines:
                                topic.result_html = topic.result_html+line
                            for line in new_lines:
                                topic.result_html = topic.result_html+line+'\n'
                        topic.page_count = max_page
                        topic.write_to_result_html()
                        await self.mongo.store_topic(topic)
            except Exception as e:
                traceback.print_exc()
                logging.info('%d请求失败', topic.tid)

    async def start(self, topic, refresh_old_html=False):
        page1,alredy_exits = await self.request.get_page(topic.tid,1,topic_title=topic.title)
        soup = bs(page1, 'lxml')
        topic.title = await parser.get_title(soup)
        topic.page_count = await parser.get_page_count(soup)
        if not os.path.exists(f'htmls/{topic.title}'):
            logging.info('创建文件夹%s', topic.title)
            os.mkdir(f'htmls/{topic.title}')
        if not alredy_exits:
            with open(f'htmls/{topic.title}/{topic.title}1.html', 'w', encoding="gbk") as f:
                f.write(page1)
                logging.info('写入%s1.html', topic.title)
        logging.info('开始解析%s第1页', topic.title)
        topic.result_html += await parser.page_parser(soup, 1, topic)
        for i in range(2, topic.page_count+1):
            logging.info('开始请求%s%d.html', topic.title, i)
            html,alredy_exits = await self.request.get_page(topic.tid, i, topic.title, refresh_old_html)
            if not alredy_exits:
                with open(f'htmls/{topic.title}/{topic.title}{i}.html', 'w', encoding="gbk") as f:
                    f.write(html)
                    logging.info('写入%s%d.html', topic.title, i)
            if not html=='' and html is not None:
                logging.info('开始解析%s第%d页', topic.title, i)
                soup = bs(html, 'lxml')
                topic.result_html += await parser.page_parser(soup, i, topic)
        topic.write_to_result_html()
        topic.status = Nga.TopicStatus.LIVE
        await self.mongo.store_topic(topic)

    async def get_index(self):
        r = await self.request.session.get(Nga.url_index)
        content = r.text.replace('�', '')
        with open('index.html', 'w') as f:
            f.write(content)
        soup = bs(content, 'lxml')
        list = soup.find_all('a', {'class': 'topic'})
        replies_list = soup.find_all('a', {'class': 'replies'})
        print(list[-1]['href'], list[-1].text)
        print(replies_list[-1].text)
