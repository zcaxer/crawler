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
        url=''
    class Topic:
        id=0
        authur=''
        title=''
        up=0
        content=''
        post_date=''
        last_post_date=''
        post_count=0
        page_count=0

        def __init__(self,html=None):
            pass
    class Post:
        id = 0  # 楼层
        authur=''
        content=''
        quote_from = []
        reply_from = []
        reply_to = 0
        quote_to=0
        up=0
        date=''
        reply_by=[]
        quote_by=[] 

    class User:
        id=0
        name=''
        post_number=0
        topic_number=0

    def __init__(self, id):
        self.html_list = []
        self.id = id
        self.last_post_uid = ''
        self.last_posttime = ''
        self.last_page = ''
        self.result_html = ''
