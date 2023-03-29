# class Nga
'''nga class '''
import logging


class Nga:

    p_img_partial = r'\[img\]\..+?\[/img\]?'
    p_img = r'\[img\].+?\[/img\]'
    url_img = r'https://img.nga.178.com/attachments'
    url_first_page = "https://nga.178.com/read.php?tid={id}"
    url_page = "https://nga.178.com/read.php?tid={id}&page={page}"
    url_index = "https://nga.178.com/thread.php?fid=-7"


class Section:
    url = ''


class Topic:
    ''' topic class 
    帖子内容在posts[0]'''

    def __init__(self, topic_id):
        self.id = topic_id
        self.title = ''
        self.last_post_date = ''
        self.post_count = 0
        self.page_count = 0
        self.posts=[]
        self.result_html=''

    def write_to_result_html(self):
        logging.info('开始写入%s.html', self.title)
        with open(f'results/{self.title}.html', "w", encoding='utf-8') as writer:
            writer.write(
                f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>{self.title}</title>\n</head>\n<body>\n')
            writer.write(self.result_html)
            writer.write('</body>\n</html>')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'last_post_date': self.last_post_date,
            'post_count': self.post_count,
            'page_count': self.page_count,
            'posts': [post.to_dict() for post in self.posts]
        }


class Post:
    def __init__(self, id):
        self.id = id  # 楼层
        self.author_uid = None
        self.author_name=None
        self.date = None
        self.content = None
        self.quote_to = []
        self.quote_to = None
        self.reply_to = []
        self.quote_to = None
        self.up_counts = None
        self.reply_by = []
        self.quote_by = []


    def to_dict(self):
        return {
            'reply_id': self.reply_id,
            'author': self.author,
            'date': self.date,
            'content': self.content,
            'quote_to': self.quote_to,
            'reply_to': self.reply_to,
            'up_counts': self.up_counts,
            'reply_by': self.reply_by,
            'quote_by': self.quote_by
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
