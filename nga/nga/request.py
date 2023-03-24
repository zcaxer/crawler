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
        self.mongo=Mongo()
        self.cookies=self.mongo.read_cookies()
        self.session=aiohttp.ClientSession(cookies=self.cookies)
        

    async def download_img(self,url: str, path: str, pic_name: str):
        logging.info('Downloading %s ', pic_name)
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
                    chunk=await resp.content.read(1024)
                    if not chunk:break
                    f.write(chunk)


    def get_page(self, topic_id,page: int, refresh_old_html=False):
        if page == 1:
            time.sleep(2)
            r = session.get(Nga.url_first_page.format(id=topic_id))
            if r.status_code == 403:
                logging.warning(f'第{page}页请求失败')
                return
        elif refresh_old_html == False and os.path.exists(f'htmls/{self.title}/{self.title}{page}.html'):
            with open(f'htmls/{self.title}/{self.title}{page}.html', 'r', encoding='gbk') as f:
                return f.read()
        else:
            time.sleep(2)
            r = self.session.get(Nga.url_page.format(id=self.id, page=page))
            if r.status_code == 403:
                logging.warning(f'第{page}页请求失败')
                return
        return r.text.replace('�', '')
