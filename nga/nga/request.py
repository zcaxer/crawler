''' class request
'''
import os
import logging
import time
import asyncio
import aiohttp

from .nga import Nga
from .mongo import Mongo


class Request:

    def __init__(self):
        self.mongo = Mongo()
        self.cookies = self.mongo.read_cookies()
        self.session = aiohttp.ClientSession(cookies=self.cookies)

    async def download_img(self, url: str, topic_title: str, pic_name: str):
        logging.info('Downloading %s ', pic_name)
        path=topic_title
        if not os.path.exists(f'htmls/{path}/img'):
            os.mkdir(f'htmls/{path}/img')
        if os.path.exists(f'htmls/{path}/img/{pic_name}'):
            logging.debug('%s already exists', pic_name)
            return
        if url[1] == 'm':
            url = Nga.url_img+url
        async with self.session.get(url) as resp:
            with open(f'htmls/{path}/img/{pic_name}', 'wb') as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    async def get_page(self, topic_id, page: int, topic_title=None, refresh_old_html=False, delay=2):
        if refresh_old_html == False and os.path.exists(f'htmls/{topic_title}/{topic_title}{page}.html'):
            with open(f'htmls/{topic_title}/{topic_title}{page}.html', 'r', encoding='gbk') as f:
                return f.read()
        elif page == 1:
            url = Nga.url_first_page.format(id=topic_id)
        else:
            url = Nga.url_page.format(id=topic_id, page=page)
        time.sleep(delay)
        rsps = await self.session.get(url)
        if rsps.status == 403:
            logging.warning('第%d页请求失败,403',page)
            return
        html=await rsps.text()
        return html.replace('�', '')
