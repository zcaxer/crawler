import time
import requests
import re
import os
from bs4 import BeautifulSoup as bs


id = "27525038"


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


def get_content(html, name):
    with open(name+r".txt", "a", encoding='utf-8') as w:
        soup = bs(html, 'lxml')
        try:
            l = soup.find_all(id=re.compile(r"postcontent\d+"))
            s = soup.find_all(id=re.compile(r'postauthor\d+'))
            pattern = re.compile(r'\d+')
            for i in range(0, len(l)):
                uid = pattern.findall(s[i]['href'])[0]
                w.write(uid+":"+l[i].text+"\n")
        except:
            print('get_content error')


def get_html(id, cookie):
    r = requests.get(f"https://bbs.nga.cn/read.php?tid={id}", cookies=cookie)
    html = r.text
    name, page_max = find_title(html)
    get_content(html, name)
    if not os.path.exists(name):
        os.mkdir(name)
    with open(f'{name}/{name}1.html', 'w', encoding="gbk") as f:
        f.write(r.text)
    for i in range(2, page_max):
        time.sleep(2)
        r = requests.get(
            f"https://bbs.nga.cn/read.php?tid={id}&page={i}", cookies=cookie)
        with open(f'{name}/{name}{i}.html', 'w', encoding="gbk") as f:
            f.write(r.text)
        get_content(r.text, name)


def find_title(html):
    soup = bs(html, 'lxml')
    l1 = soup.find("title").text
    pattern1 = re.compile(r'(.*)\sNGA玩家社区')
    name = pattern1.findall(l1)[0]
    l2 = soup.find(id='pageBtnHere')
    pattern2 = re.compile(r',1:(\d+)')
    page = int(pattern2.findall(l2.next_sibling.text)[0])
    return name, page


if __name__ == "__main__":
    #get_html(id, cookie)
    for i in range(1, 40):
        with open(f'firstSexNga/firstSexNga{i}.html', 'r', encoding="gbk") as f:
            get_content(f, "大家的第一次都是怎么没的")
