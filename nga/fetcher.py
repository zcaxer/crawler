import os
import json
import logging
import requests
from .nga import Nga


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
