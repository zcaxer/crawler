# class Nga
'''nga class '''
import logging
from enum import Enum


class Nga:

    p_img_partial = r'\[img\]\..+?\[/img\]?'
    p_img = r'\[img\].+?\[/img\]'
    url_img = r'https://img.nga.178.com/attachments'
    url_first_page = "https://nga.178.com/read.php?tid={id}"
    url_page = "https://nga.178.com/read.php?tid={id}&page={page}"
    url_index = "https://nga.178.com/thread.php?fid=-7"


class TopicState(Enum):
    NEW = 0
    LIVE = 1
    DEAD = 2

class Section:
    url = ''


class Topic:
    ''' topic class 
    帖子内容在posts[0]'''

    def __init__(self, topic_id):
        self.tid = topic_id
        self.title = ''
        self.last_post_date = ''
        self.post_count = 0
        self.page_count = 0
        self.posts=[]
        self.result_html=''
        self.html=''
        self.state=TopicState.NEW

    def write_to_result_html(self):
        logging.info('开始写入%s.html', self.title)
        with open(f'results/{self.title}.html', "w", encoding='utf-8') as writer:
            writer.write(
                f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>{self.title}</title>\n</head>\n<body>\n')
            writer.write(self.result_html)
            writer.write('</body>\n</html>')

    def to_dict(self):
        return {
            'tid': self.tid,
            'title': self.title,
            'last_post_date': self.last_post_date,
            'post_count': self.post_count,
            'page_count': self.page_count,
        }

    def add_post(self, post):
            self.posts.append(post)
            self.post_count += 1
            self.last_post_date = post.date

    def find_post_id_by_author_id_and_date(self, author_id, date):
        for post in self.posts:
            if post.author_id == author_id and post.date == date:
                return post.pid
        return None


class Post:
    def __init__(self, pid):
        self.pid = pid  # 楼层
        self.author_id = 0
        self.author_name=''
        self.date = None
        self.content = None
        self.quote_to = []
        self.reply_to = []
        self.up_counts = 0
        self.replied_by = []
        self.quoted_by = []


    def to_dict(self):
        return {
            'pid': self.pid,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'date': self.date,
            'content': self.content,
            'quote_to': self.quote_to,
            'reply_to': self.reply_to,
            'up_counts': self.up_counts,
            'replied_by': self.replied_by,
            'quoted_by': self.quoted_by
        }

class User:
    uid = 0
    name = ''
    post_number = 0
    topic_number = 0

    def __init__(self, uid):
        self.html_list = []
        self.uid = uid
        self.last_post_uid = ''
        self.last_posttime = ''
        self.last_page = ''
        self.result_html = ''
