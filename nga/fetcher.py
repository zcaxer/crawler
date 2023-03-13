import os
import json
import logging
import requests
from nga import Nga


def get_session():
    with open('nga.json', 'r', encoding='utf-8') as config_file:
        nga_json = json.load(config_file)
    cookie_jar = requests.utils.cookiejar_from_dict(nga_json['cookies'])
    session = requests.Session()
    session.cookies = cookie_jar
    return session


def download_img(session,url: str, path: str, pic_name: str):
    logging.info('Downloading %s ', pic_name)
    if not os.path.exists(f'htmls/{path}/img'):
        os.mkdir(f'htmls/{path}/img')
    if os.path.exists(f'htmls/{path}/img/{pic_name}'):
        logging.debug('%s already exists', pic_name)
        return
    if url[1] == 'm':
        url = Nga.url_img+url
    with open(f'htmls/{path}/img/{pic_name}', 'wb') as f:
        f.write(session.get(url).content)
