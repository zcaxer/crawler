''' class request
'''
import os
import logging
import aiohttp

from .nga import Nga
from .mongo import Mongo

class Request:

    def __init__(self):
        self.mongo=Mongo()
        self.session = self.get_session()

    async def get_session(self):
        with open('nga.json', 'r', encoding='utf-8') as f:
            cookies=await self.mongo.read_cookie()
            session = aiohttp.ClientSession(cookies=cookies)  
            return session

    @classmethod
    def download_img(cls,url: str, path: str, pic_name: str):
        logging.info('Downloading %s ', pic_name)
        if not os.path.exists(f'htmls/{path}/img'):
            os.mkdir(f'htmls/{path}/img')
        if os.path.exists(f'htmls/{path}/img/{pic_name}'):
            logging.debug('%s already exists', pic_name)
            return
        if url[1] == 'm':
            url = Nga.url_img+url
        with open(f'htmls/{path}/img/{pic_name}', 'wb') as f:
            f.write(cls.session.get(url).content)


    def get_page(self, page: int, refresh_old_html=False):
        if page == 1:
            time.sleep(2)
            r = session.get(Nga.url_first_page.format(id=self.id))
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
