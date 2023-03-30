import time
import re
import os
import traceback
import argparse
import asyncio
import json
import logging
import requests
from bs4 import BeautifulSoup as bs
import aiofiles

from nga.request import Request
from nga.mongo import Mongo
from nga.nga import Nga,Topic,TopicState
import nga.parser as parser

# TODO:查找回复内容原文并展示
# TODO:重构，单元化
# TODO:update posts
# TODO:find post I interested in


class Topic_clawler:
    request=None
    mongo=None
    topics=[]
    def __init__(self, topic_id_list):
        if self.request is None:
            self.request=Request()
        if self.mongo is None:
            self.mongo=Mongo()
        for i in topic_id_list:
            self.topics.append(Topic(i))

    @classmethod
    def init(cls):
        with open('nga.json', 'r', encoding='utf-8') as f:
            cls.json = json.load(f)
            cls.new_ids = cls.json['new_ids']
            cls.ongoing_ids: dict = cls.json['ongoing_ids']
            cls.finished_ids: dict = cls.json['finished_ids']

    def __del__(self):
        cookie_jar = self.request.session.cookie_jar
        cookies = {cookie.key: cookie.value for cookie in cookie_jar}
        self.mongo.store_cookies(cookies)
        self.request.session.close()
        self.mongo.async_client.close()
        self.mongo.sync_client.close()

    def update(self):
        keys = list(self.ongoing_ids.keys())
        for id in keys:
            try:
                page = self.ongoing_ids[id]['last_page']
                time.sleep(1)
                rsps = self.request.get(Nga.url_page.format(id=id, page=page))
                soup = bs(rsps.text, 'lxml')
                t = soup.title.text
                if t == '找不到主题' or t == "帖子发布或回复时间超过限制" or t == "帖子被设为隐藏" or t == '帖子审核未通过' :
                    #or t == "帖子正等待审核":
                    self.json['finished_ids'].update({id: self.ongoing_ids[id]})
                    self.json['ongoing_ids'].pop(id)
                    logging.info(f'id:{id} finished')
                else:
                    s_posttime = soup.find_all('div', {'class': 'postInfo'})
                    last_posttime = s_posttime[-1].text
                    if last_posttime != self.ongoing_ids[id]['last_time']:
                        max_page = parser.get_max_page(soup)
                        nga_clawler = Topic_clawler(id)
                        nga_clawler.title = self.ongoing_ids[id]['title']
                        for p in range(page, max_page+1):
                            html =self.request.get_page(id, p)
                            with open(f'htmls/{nga_clawler.title}/{nga_clawler.title}{p}.html', 'w', encoding="gbk") as f:
                                f.write(html)
                                logging.info(f'写入{nga_clawler.title}{p}.html')
                            nga_clawler.get_content(p, html)

                        with open(f'results/{nga_clawler.title}.html', "r", encoding='utf-8') as r:
                            old_lines = r.readlines()[7:-2]
                            new_lines = nga_clawler.result_html.splitlines()
                            pattern = re.compile(
                                '\s*\<\s*p\s*\>\s*(\d+)\s*:.*\<\s*/p\s*\>\s*')
                            while True:
                                n = int(pattern.match(new_lines[0]).group(1))
                                if n <= int(self.ongoing_ids[id]['last_post']):
                                    new_lines.pop(0)
                                else:
                                    break
                            nga_clawler.result_html = ''
                            for line in old_lines:
                                nga_clawler.result_html = nga_clawler.result_html+line
                            for line in new_lines:
                                nga_clawler.result_html = nga_clawler.result_html+line+'\n'
                        nga_clawler.page_count = max_page
                        nga_clawler.write_to_result_html()
                        nga_clawler.finish()
                Topic_clawler.dump()
            except Exception as e:
                traceback.print_exc()
                logging.info(f'{id}请求失败')    

    async def start(self,topic,refresh_old_html=False):
        page1 =await self.request.get_page(topic.id, 1)
        soup = bs(page1, 'lxml')
        topic.title=await parser.get_title(soup)
        topic.page_count =await parser.get_page_count(soup)
        if not os.path.exists(topic.title):
            logging.info('创建文件夹%s',topic.title)
            os.mkdir(f'htmls/{self.title}')
        with open(f'htmls/{topic.title}/{self.title}1.html', 'w', encoding="gbk") as f:
            f.write(page1)
            logging.info('写入%s1.html',topic.title)
        logging.info('开始解析%s第1页',self.title)
        topic.result_html += await parser.page_parser(soup, 1, topic)
        for i in range(2, topic.page_count+1):
            logging.info('开始请求%s%d.html',self.title,i)
            html = self.request.get_page(topic.id,i, refresh_old_html)
            with open(f'htmls/{self.title}/{self.title}{i}.html', 'w', encoding="gbk") as f:
                f.write(html)
                logging.info('写入%s%d.html',self.title,i)
            logging.info('开始解析%s第%d页',self.title,i)
            soup=bs(html, 'lxml')
            topic.result_html+=await parser.page_parser(soup, i,topic)
        topic.write_to_result_html()
        topic.state=TopicState.LIVE
        await self.mongo.store_topic(topic)


    def get_index(self):
        r = self.request.get(Nga.url_index)
        content = r.text.replace('�', '')
        with open('index.html', 'w') as f:
            f.write(content)
        soup = bs(content, 'lxml')
        list = soup.find_all('a', {'class': 'topic'})
        replies_list = soup.find_all('a', {'class': 'replies'})
        print(list[-1]['href'], list[-1].text)
        print(replies_list[-1].text)


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    arg_parser=argparse.ArgumentParser(description="nga 爬虫")
    arg_parser.add_argument('-u','--update',action='store_true',help='更新爬虫库中的帖子')
    arg_parser.add_argument('-f','--force',action='store_true',help='强制更新该id的帖子')
    arg_parser.add_argument('id',metavar='ID', nargs='*',type=int)
    args=arg_parser.parse_args()

    if args.update :
        Topic_clawler.update()
    print(args)    
    nga_clawler = Topic_clawler(args.id)
    for i in nga_clawler.topics:
        topic=Topic(i)
        topic.state=nga_clawler.start(topic)

    #Nga.start_new()
    topic_clawler.get_index()
