import time
from numpy import unicode_
import requests
import re
import os
from bs4 import BeautifulSoup

id = "30902165"

url = "https://bbs.nga.cn/read.php?tid={id}&page="
name = "五年不见，你还会梦到她吗"
page=4

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


def get_html(id, page, name, cookie):
	r = requests.get(f"https://bbs.nga.cn/read.php?tid={id}", cookies=cookie)
	r = requests.get(f"https://bbs.nga.cn/read.php?tid={id}&page={page}", cookies=cookie)
	with open(f'{name}/{name}{page}.html', 'w',encoding="gbk") as f:
		f.write(r.text)


def get_content(page,name):
	with open(name+r".txt", "a", encoding='utf-8') as w:
		with open(f'{name}/{name}{page}.html', 'r', encoding='gbk') as f:
			soup = BeautifulSoup(f, 'lxml')
			for i in range(20*(page-1), 20*page):
				try:
					l = soup.find(id=f"postcontent{i}")
					s = soup.find(id=f'postauthor{i}')["href"]
					pattern = re.compile(r'\d+')
					uid = pattern.findall(s)[0]
					w.write(uid+":"+l.text+"\n")
				except:
					pass




if not os.path.exists(name):
	os.mkdir(name)
for i in range(1, page+1):
	get_html(id,i,name,cookie)
	time.sleep(2)	
	get_content(i,name)
	
