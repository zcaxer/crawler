# class Nga
'''nga class '''
import logging
from enum import Enum
from .mongo import Mongo




class Nga:
    mongo = None
    p_img_partial = r'\[img\]\..+?\[/img\]?'
    p_img = r'\[img\].+?\[/img\]'
    url_img = r'https://img.nga.178.com/attachments'
    url_first_page = "https://nga.178.com/read.php?tid={id}"
    url_page = "https://nga.178.com/read.php?tid={id}&page={page}"
    url_index = "https://nga.178.com/thread.php?fid=-7"

    def __init__(self):
        if Nga.mongo is None:
            Nga.mongo = Mongo()

    class TopicStatus(Enum):
        NEW = 0
        LIVE = 1
        DEAD = 2


    class Section:
        url = ''


    class Topic:
        ''' topic class 
        帖子内容在posts[0]'''

        def __init__(self, topic_id, page_count=0, last_post_date=None, last_post_index=0, title=None):
            self.tid = topic_id
            self.title = title
            self.last_post_date = last_post_date
            self.post_count = 0  # 回复数，不再存入db，若需要从db中查询
            self.last_post_index = last_post_index  # 最后回复的楼层
            self.page_count = page_count
            self.posts = []
            self.result_html = ''
            self.html = ''
            self.status = Nga.TopicStatus.NEW
            if Nga.mongo is None:
                Nga.mongo = Mongo()

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
                'last_post_index': self.last_post_index,
                'page_count': self.page_count,
                'status': self.status.value,
            }

        def add_post(self, post,new=False):
            n = post.index - len(self.posts)
            if n > 0:
                self.posts = self.posts+[None]*n
            self.posts.append(post)
            if new:
                self.last_post_date = post.date
                self.last_post_index = post.index

        def search_post_in_list(self, post_pid):
            for post in self.posts:
                if post is None:
                    continue
                elif post.pid == post_pid:
                    return post
            return None

        async def search_post(self, post_pid):
            post=self.search_post_in_list(post_pid)
            if post is None:
                post_dict= await Nga.mongo.search_post(self.tid,post_pid)
                if post_dict is None:
                    return None
                post = Nga.Post(post_dict)
                self.add_post(post)
            return post


    class Post:
        def post_from_dict(self, info_dict:dict):
            if info_dict is not None:
                self.index = info_dict.get('index',None)  # 楼层
                self.pid = info_dict.get('pid', None)  # 帖子id，
                self.author_id = info_dict.get('author_id', None)
                self.author_name = info_dict.get('author_name', None)
                self.date = info_dict.get('date', None)
                self.content = info_dict.get('content', None)
                self.quote_to = info_dict.get('quote_to', None)
                self.reply_to = info_dict.get('reply_to', None)
                self.up_count = info_dict.get('up_count', None)
                self.replied_by = info_dict.get('replied_by', None)
                self.quoted_by = info_dict.get('quoted_by', None)


        def __init__(self, index_or_dict, pid=0, author_id=0, author_name='', date=None, content='',up_count=0):
            if isinstance(index_or_dict, dict):
                self.post_from_dict(index_or_dict)   
            else:
                self.index = index_or_dict
                self.pid = pid
                self.author_id = author_id
                self.author_name = author_name
                self.date = date
                self.content = content
                self.quote_to = None
                self.reply_to = None
                self.up_count = up_count
                self.replied_by = []
                self.quoted_by = []

        def to_dict(self):
            return {
                'pid': self.pid,
                'index': self.index,
                'author_id': self.author_id,
                'author_name': self.author_name,
                'date': self.date,
                'content': self.content,
                'quote_to': self.quote_to,
                'reply_to': self.reply_to,
                'up_count': self.up_count,
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
