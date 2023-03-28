# class Nga
'''nga class '''


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
    def __init__(self, reply_id, author, post_date, content, up_counts, reply_to=None, quote_to=None):
        self.reply_id = reply_id  # 楼层
        self.author = author
        self.date = post_date
        self.content = content
        if reply_to is None:
            self.quote_to = []
        else:
            self.quote_to = quote_to
        if quote_to is None:
            self.reply_to = []
        else:
            self.quote_to = quote_to
        self.up_counts = up_counts
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
