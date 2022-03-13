import time
import requests
import re
import os
import json
from bs4 import BeautifulSoup as bs

# TODO:查找回复内容原文并展示
# TODO:ac娘
# TODO:update posts
# TODO:find post I interested in


p_img_partial = '\[img\]\..+?\[/img\]?'
p_img = '\[img\].+?\[/img\]'
ulr_img = 'https://img.nga.178.com/attachments'

id = "30844033"
#l=['31022622','30902165', '30929995', '30938217','30844033','30627975','29688508']
l = [  '30312817', '30605933','31008448',
'31014291', '31003175','31000123', '30993134', '30993134',
     '30931300','30956222']


cookie = {
    "bbsmisccookies": "{\"uisetting\":{0:1,1:1652928767},\"pv_count_for_insad\":{0:-47,1:1646326827},\"insad_views\":{0:1,1:1646326827}}",
    "lastpath": "/thread.php?fid=-7",
    "lastvisit": "1646273592",
                "ngacn0comInfoCheckTime": "1646273561",
                "ngacn0comUserInfo": "zyphaxy\tzyphaxy\t39\t39\t\t10\t0\t4\t0\t0\t",
                "ngacn0comUserInfoCheck": "2d6fcde163dbe7dab3f2ca34c02fd60b",
                "ngaPassportCid": "X8rrnqig4bke1khjjeru6fbs5dktmnmo13volni6",
                "ngaPassportUid": "61056884",
                "ngaPassportUrlencodedUname": "zyphaxy"
}


def write_html_head(f, title):
    f.write(
        f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>{title}</title>\n</head>\n<body>\n')


def download_img(url: str, path: str, pic_name: str):
    url_img = 'https://img.nga.178.com/attachments'
    if not os.path.exists(f'{path}/img'):
        os.mkdir(f'{path}/img')
    if os.path.exists(f'{path}/img/{pic_name}'):
        return
    if url[1] == 'm':
        url = url_img+url
    with open(f'{path}/img/{pic_name}', 'wb') as f:
        f.write(requests.get(url).content)


def img_content_processor(content: str, title):
    pattern_img = re.compile(r'(.*?)\[img\]\.?(.+?)\[/img\](.*?)')
    match_img = pattern_img.findall(content)
    if not match_img:
        return content
    pattern_pic_name = re.compile(r'.*/(.*?\..*?)$')
    content = ''
    for i in match_img:
        pic_name = pattern_pic_name.search(i[1]).group(1)
        download_img(i[1], title, pic_name)
        content += f'{i[0]}<img src="{title}/img/{pic_name}">{i[2]}'
    return content


def content_processor(content, f):
    s = ''
    pattern_quote = re.compile(
        'Post by \[uid=\d+\](.*)\[/uid\] \(.*\):\[/b\](.*)\[\/quote\](.*)')
    match_quote = pattern_quote.search(content)
    if match_quote:
        quote_uname = match_quote.groups()[0]
        quote_content = match_quote.groups()[1]
        reply_content = match_quote.groups()[2]
        s += f'<blockquote><p>{quote_uname}:{quote_content}</p></blockquote>{reply_content}\n'
        return s
    pattern_reply = re.compile(
        '\[b\]Reply to \[pid=\d+,\d+,\d+\]Reply\[/pid\] Post by \[uid=\d+\](.*)\[/uid\] \((.*)\)\[/b\](.*)')
    match_reply = pattern_reply.search(content)
    if match_reply:
        post_uname = match_reply.groups()[0]
        post_time = match_reply.groups()[1]
        reply_content = match_reply.groups()[2]
        #print(post_uname, post_time)
        pattern_post_content = re.compile(
            f'<p>\d+:{post_uname},{post_time},\d+,up:\d+:<br>(.*)</p>')
        post_content = '未匹配到'
        f.seek(0)
        for line in f:
            match = pattern_post_content.search(line)
            if match:
                post_content = match.group(1)
                break
        s += f'<blockquote><p>{post_uname}:{post_content}</p></blockquote>{reply_content}\n'
        return s
    return content


def get_content(f, html, title):
    soup = bs(html, 'lxml')
    pattern_uid = re.compile(r'\d+')
    pattern_userInfo = re.compile(
        'commonui\.userInfo\.setAll\(\s+(.*)\)')
    pattern_content = re.compile(r"postcontent(\d+)")
    pattern_up_str = re.compile('ngaAds\.bbs_ads8_load_new')
    pattern_up = re.compile("'\d+,(\d+),\d+")
    s_uid = soup.find_all(id=re.compile(r'postauthor\d+'))
    s_posttime = soup.find_all('div', {'class': 'postInfo'})
    s_content = soup.find_all(id=pattern_content)
    s_up_number = soup.find_all('script', text=pattern_up_str)
    s_userInfos = soup.find(
        'script', {'type': 'text/javascript'}, text=pattern_userInfo)
    userInfos = pattern_userInfo.findall(s_userInfos.text)
    j = json.loads(userInfos[0])
    for i in range(0, len(s_content)):
        uid = pattern_uid.search(s_uid[i]['href']).group()
        id = pattern_content.search(s_content[i].get('id')).group(1)
        username = j[uid]['username'] if(uid in j) else '匿名'
        posttime = s_posttime[i].text
        content = s_content[i].text
        up_number = pattern_up.search(s_up_number[i].text).group(1)
        content = img_content_processor(content, title)
        content = content_processor(content, f)
        f.write(
            f'<p>{id}:{username},{posttime},{uid},up:{up_number}:<br>{content}</p>\n')


def get_title(html):
    soup = bs(html, 'lxml')
    l1 = soup.find("title").text
    pattern1 = re.compile(r'(.*)\sNGA玩家社区')
    title = pattern1.findall(l1)[0]
    l2 = soup.find(id='pageBtnHere')
    pattern2 = re.compile(r',1:(\d+)')
    max_page = int(pattern2.findall(l2.next_sibling.text)[0])
    return title, max_page


def get_html(id, cookie):
    r = requests.get(f"https://bbs.nga.cn/read.php?tid={id}", cookies=cookie)
    if r.status_code == 403:
        print(f'{id}请求失败')
        return
    html = r.text
    title, max_page = get_title(html)
    if not os.path.exists(title):
        os.mkdir(title)
    with open(f'{title}/{title}1.html', 'w', encoding="gbk") as f:
        write_html_head(f, title)
        f.write(r.text)
    with open(title+r".html", "a+", encoding='utf-8') as w:
        write_html_head(w, title)
        get_content(w, html, title)
        for i in range(2, max_page+1):
            time.sleep(2)
            r = requests.get(
                f"https://bbs.nga.cn/read.php?tid={id}&page={i}", cookies=cookie)
            with open(f'{title}/{title}{i}.html', 'w', encoding="gbk") as f:
                f.write(r.text)
            get_content(w, r.text, title)
        w.write('</body>\n</html>')


def get_content_from_html(title):
    for i in range(1, 40):
        with open(f'{title}/{title}{i}.html', 'r', encoding="gbk") as f:
            get_content(f, title)


def update(l):
    for i in l:
        pass


if __name__ == "__main__":
    for i in l:
        get_html(i, cookie)
