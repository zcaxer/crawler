import time
import requests
import re
import os
import json
import logging
from bs4 import BeautifulSoup as bs
import aiofiles
import traceback

# TODO:查找回复内容原文并展示
# TODO:ac娘
# TODO:重构，单元化
# TODO:update posts
# TODO:find post I interested in


class Nga:

    p_img_partial = '\[img\]\..+?\[/img\]?'
    p_img = '\[img\].+?\[/img\]'
    url_img = 'https://img.nga.178.com/attachments'
    url_first_page = "https://nga.178.com/read.php?tid={id}"
    url_page = "https://nga.178.com/read.php?tid={id}&page={page}"

    def __init__(self, id):
        self.html_list = []
        self.id = id
        self.last_post_uid = ''
        self.last_posttime = ''
        self.last_page = ''
        self.result_html=''

    @classmethod
    def init(cls):
        with open('nga.json', 'r',encoding='utf-8') as f:
            cls.json = json.load(f)
            cls.new_ids = cls.json['new_ids']
            cls.ongoing_ids: dict = cls.json['ongoing_ids']
            cls.finished_ids: dict = cls.json['finished_ids']
            cls.cookieJar = requests.utils.cookiejar_from_dict(
                cls.json['cookies'])
            cls.session = requests.Session()
            cls.session.cookies = cls.cookieJar

    @classmethod
    def start_new(cls):
        for id in cls.new_ids:
            nga=Nga(id)
            nga.start()

    @classmethod
    def update(cls):
        for id in cls.ongoing_ids.keys():
            try:
                page = cls.ongoing_ids[id]['last_page']
                r = cls.session.get(cls.url_page.format(id=id, page=page))
                soup = bs(r.text, 'lxml')
                if soup.title == '找不到主题':
                    cls.json['finished_ids'].update({id: cls.ongoing_ids[id]})
                    cls.json['ongoing_ids'].pop(id)
                    logging.info(f'id:{id} finished')
                else:
                    s_posttime = soup.find_all('div', {'class': 'postInfo'})
                    last_posttime = s_posttime[-1].text
                    if last_posttime != cls.ongoing_ids[id]['last_time']:
                        max_page = Nga.get_max_page(soup)
                        nga=Nga(id)
                        nga.title=cls.ongoing_ids[id]['title']
                        for p in range(page, max_page+1):
                            html=nga.get_page(p,True)
                            with open(f'{nga.title}/htmls/{nga.title}{p}.html', 'w', encoding="gbk") as f:
                                f.write(html)
                                logging.info(f'写入{nga.title}{p}.html')
                            nga.get_content(p,html)
                        
                        with open(f'results/{nga.title}.html', "r", encoding='utf-8') as r:
                            old_lines=r.readlines()[7:-2]
                            new_lines=nga.result_html.splitlines()
                            pattern = re.compile(
                                '\s*\<\s*p\s*\>\s*(\d+)\s*:.*\<\s*/p\s*\>\s*')
                            while True:
                                n=int(pattern.match(new_lines[0]).group(1))    
                                if n <= int(cls.ongoing_ids[id]['last_post']):
                                    new_lines.pop(0)
                                else:break
                            nga.result_html=''
                            for line in old_lines:
                                nga.result_html = nga.result_html+line
                            for line in new_lines:
                                nga.result_html = nga.result_html+line+'\n'
                        nga.last_page=max_page
                        nga.write_to_result_html()
                        nga.finish()
                        Nga.dump()
            except Exception as e:
                traceback.print_exc()
                logging.info(f'{id}请求失败')


    def download_img(self, url: str, path: str, pic_name: str):
        logging.info(f'Downloading {pic_name}')
        if not os.path.exists(f'{path}/img'):
            os.mkdir(f'{path}/img')
        if os.path.exists(f'{path}/img/{pic_name}'):
            logging.debug(f'{pic_name} already exists')
            return
        if url[1] == 'm':
            url = Nga.url_img+url
        with open(f'htmls/{path}/img/{pic_name}', 'wb') as f:
            f.write(self.session.get(url).content)

    def img_post_content_processor(self, post_content: str):

        logging.info(f'Processing {self.title} img url')
        pattern_img = re.compile(r'(.*?)\[img\]\.?(.+?)\[/img\](.*?)')
        match_img = pattern_img.findall(post_content)
        if not match_img:
            return post_content
        pattern_pic_name = re.compile(r'.*/(.*?\..*?)$')
        post_content = ''
        for i in match_img:
            pic_name = pattern_pic_name.search(i[1]).group(1)
            self.download_img(i[1], self.title, pic_name)
            post_content += f'{i[0]}<img src="{self.title}/img/{pic_name}">{i[2]}'
        return post_content

    def post_processor(self, original_post_content):
        logging.info('开始处理引用和回复')
        post_content = ''
        pattern_quote = re.compile(
            '\[b\]\s*Post\s*by\s*\[uid=?\d*\](.*)\[/uid\].*\(.*\):\[/b\](.*)\[\/quote\](.*)')
        match_quote = pattern_quote.search(original_post_content)
        if match_quote:
            logging.debug('引用')
            quote_uname = match_quote.groups()[0]
            quote_content = match_quote.groups()[1]
            reply_content = match_quote.groups()[2]
            post_content += f'<blockquote><p>{quote_uname}:{quote_content}</p></blockquote>{reply_content}'
            return post_content
        pattern_reply = re.compile(
            '\[b\]Reply to \[pid=\d+,\d+,\d+\]Reply\[/pid\] Post by \[uid=?\d*\](.*)\[/uid\] \((.*)\)\[/b\](.*)')
        match_reply = pattern_reply.search(original_post_content)
        if match_reply:
            logging.debug('回复')
            post_uname = match_reply.groups()[0]
            post_time = match_reply.groups()[1]
            reply_content = match_reply.groups()[2]
            #print(post_uname, post_time)
            pattern_post_content = re.compile(
                f'<p>\d+:{post_uname},{post_time},\d+,up:\d+:<br>(.*)\n?</p>\s')
            original_post_content = '未匹配到'
            match = pattern_post_content.search(self.result_html)
            if match:
                original_post_content = match.group(1)                    
            post_content += f'<blockquote><p>{post_uname}:{original_post_content}</p></blockquote>{reply_content}'
            return post_content
        return original_post_content

    def get_content(self, page,html=None):
        logging.debug(f'开始解析第{page}页')
        html=html or self.html_list[page-1]
        soup = bs(html, 'lxml')
        pattern_uid = re.compile(r'\d+')
        pattern_userInfo = re.compile(
            'commonui\.userInfo\.setAll\(\s+(.*)\)')
        pattern_post_content = re.compile(r"postcontent(\d+)")
        pattern_up_str = re.compile('ngaAds\.bbs_ads8_load_new')
        pattern_up = re.compile("'\d+,(\d+),\d+")
        s_uid = soup.find_all(id=re.compile(r'postauthor\d+'))
        s_posttime = soup.find_all('div', {'class': 'postInfo'})
        s_post_content = soup.find_all(id=pattern_post_content)
        s_up_number = soup.find_all('script', text=pattern_up_str)
        s_userInfos = soup.find(
            'script', {'type': 'text/javascript'}, text=pattern_userInfo)
        userInfos = pattern_userInfo.findall(s_userInfos.string)
        j = json.loads(userInfos[0],strict=False)
        for i in range(0, len(s_post_content)):
            uid = pattern_uid.search(s_uid[i]['href']).group()
            self.last_post_uid = pattern_post_content.search(
                s_post_content[i].get('id')).group(1)
            username = j[uid]['username'] if (uid in j) else '匿名'
            self.last_posttime = s_posttime[i].text
            post_content = s_post_content[i].text
            up_number = pattern_up.search(s_up_number[i].string).group(1)
            post_content = self.img_post_content_processor(post_content)
            post_content = self.post_processor(post_content)
            self.result_html =self.result_html+f'<p>{self.last_post_uid}:{username},{self.last_posttime},{uid},up:{up_number}:<br>{post_content}</p>\n'
        logging.info(f'第{page}页解析完成')

    def get_title(self):
        logging.info('开始解析标题')
        l1 = self.soup.find("title").text
        pattern1 = re.compile(r'(.*)\s178')
        self.title = pattern1.findall(l1)[0]
        l2 = self.soup.find(id='pageBtnHere')
        logging.info(f'标题解析完成,title:{self.title}')

    @staticmethod
    def get_max_page(soup):
        try:
            l = soup.find(id='pageBtnHere').next_sibling.string
            pattern2 = re.compile(r',1:(\d+)')
            last_page = int(pattern2.findall(l)[0])
        except:
            last_page=1
        logging.info(f'标题最大页数完成,last_page:{last_page}')
        return last_page

    def get_page(self, page: int, refresh_old_html=False):
        if page == 1:
            time.sleep(2)
            r = self.session.get(self.url_first_page.format(id=self.id))
            if r.status_code == 403:
                logging.warning(f'第{page}页请求失败')
                return
        elif refresh_old_html == False and os.path.exists(f'{self.title}/{self.title}{page}.html'):
            with open(f'htmls/{self.title}/{self.title}{page}.html', 'r', encoding='gbk') as f:
                return f.read()
        else:
            time.sleep(2)
            r = self.session.get(self.url_page.format(id=self.id, page=page))
            if r.status_code == 403:
                logging.warning(f'第{page}页请求失败')
                return
        return r.text.replace('�', '')

    def start(self, refresh_old_html=False):
        page1 = self.get_page(1, refresh_old_html)
        self.html_list.append(page1)
        self.soup = bs(self.html_list[0], 'lxml')
        self.get_title()
        self.last_page = self.get_max_page(self.soup)
        if not os.path.exists(self.title):
            logging.info(f'创建文件夹{self.title}')
            os.mkdir(self.title)
        with open(f'htmls/{self.title}/{self.title}1.html', 'w', encoding="gbk") as f:
            f.write(page1)
            logging.info(f'写入{self.title}1.html')
            logging.info(f'开始解析{self.title}第1页')
            self.get_content(1)
            for i in range(2, self.last_page+1):
                logging.info(f'开始请求{self.title}{i}.html')
                html = self.get_page(i, refresh_old_html)
                with open(f'htmls/{self.title}/{self.title}{i}.html', 'w', encoding="gbk") as f:
                    f.write(html)
                    logging.info(f'写入{self.title}{i}.html')
                logging.info(f'开始解析{self.title}第{i}页')
                self.html_list.append(html)
                self.get_content(i)
        self.write_to_result_html()
        self.finish()

    def finish(self):
        self.info = {"title":self.title,"last_page": self.last_page,
                          'last_post': self.last_post_uid, "last_time": self.last_posttime}
        Nga.json['ongoing_ids'][self.id] = self.info
        if self.id in Nga.json["new_ids"]:
            Nga.json["new_ids"].remove(self.id)
        
    @classmethod
    def dump(cls):
        with open('nga.json', 'w',encoding='utf-8') as w:
            cls.json['cookies']= requests.utils.dict_from_cookiejar(cls.cookieJar)
            json.dump(Nga.json, w, ensure_ascii=False)

    def write_to_result_html(self):
        logging.info(f'开始写入{self.title}.html')
        with open(f'results/{self.title}.html', "w", encoding='utf-8') as writer:
            writer.write(
                f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>{self.title}</title>\n</head>\n<body>\n')
            writer.write(self.result_html)
            writer.write('</body>\n</html>')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Nga.init()
    Nga.update()
    Nga.start_new()
    Nga.dump()

