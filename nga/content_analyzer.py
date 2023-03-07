# content analyzer

"""deal with texts and pics"""

import logging
import re
import os
from .nga import Nga

def download_img(nga:Nga, url: str, path: str, pic_name: str):
    logging.info('Downloading %s ',pic_name)
    if not os.path.exists(f'htmls/{path}/img'):
        os.mkdir(f'htmls/{path}/img')
    if os.path.exists(f'htmls/{path}/img/{pic_name}'):
        logging.debug('%s already exists', pic_name)
        return
    if url[1] == 'm':
        url = Nga.url_img+url
    with open(f'htmls/{path}/img/{pic_name}', 'wb') as f:
        f.write(nga.session.get(url).content)


def img_post_content_processor(nga:Nga,post_content: str):
    # logging.info(f'Processing {self.title} img url')
    # logging.info(f'Processing {self.title} img url')
    pattern_img = re.compile(r'(.*?)\[img\]\.?(.+?)\[/img\](.*?)')
    match_img = pattern_img.findall(post_content)
    if not match_img:
        return post_content
    pattern_pic_name = re.compile(r'.*/(.*?\..*?)$')
    post_content = ''
    for i in match_img:
        pic_name = pattern_pic_name.search(i[1]).group(1)
        download_img(nga,i[1], nga.title, pic_name)
        post_content += f'{i[0]}<img src="../htmls/{nga.title}/img/{pic_name}">{i[2]}'
    return post_content


def post_processor(nga:Nga, original_post_content):
    logging.info('开始处理引用和回复')
    post_content = ''
    pattern_quote = re.compile(
        r'\[b\]\s*Post\s*by\s*\[uid=?\d*\](.*)\[/uid\].*\(.*\):\[/b\](.*)\[\/quote\](.*)')
    match_quote = pattern_quote.search(original_post_content)
    if match_quote:
        logging.debug('引用')
        quote_uname = match_quote.groups()[0]
        quote_content = match_quote.groups()[1]
        reply_content = match_quote.groups()[2]
        post_content += f'<blockquote><p>{quote_uname}:{quote_content}</p></blockquote>{reply_content}'
        return post_content
    pattern_reply = re.compile(
        r'\[b\]Reply to \[pid=\d+,\d+,\d+\]Reply\[/pid\] Post by \[uid=?\d*\](.*)\[/uid\] \((.*)\)\[/b\](.*)')
    match_reply = pattern_reply.search(original_post_content)
    if match_reply:
        logging.debug('回复')
        post_uname = match_reply.groups()[0]
        post_time = match_reply.groups()[1]
        reply_content = match_reply.groups()[2]
        # print(post_uname, post_time)
        pattern_post_content = re.compile(
            rf'<p>\d+:{post_uname},{post_time},\d+,up:\d+:<br>(.*)\n?</p>\s')
        original_post_content = '未匹配到'
        match = pattern_post_content.search(nga.result_html)
        if match:
            original_post_content = match.group(1)
        post_content += f'<blockquote><p>{post_uname}:{original_post_content}</p></blockquote>{reply_content}'
        return post_content
    return original_post_content
