from bs4 import BeautifulSoup as bs
import re
import json


def get_content(html, name):
    with open(name+r".txt", "a", encoding='utf-8') as w:
        soup = bs(html, 'lxml')

        pattern1 = re.compile(r'\d+')
        pattern2 = re.compile(r"postcontent(\d+)")
        pattern3 = re.compile('commonui\.userInfo\.setAll\(\s+(.*)\)')
        s2 = soup.find_all(id=re.compile(r'postauthor\d+'))
        s1 = soup.find_all(id=pattern2)
        s3 = soup.find(
            'script', {'type': 'text/javascript'}, text=pattern3)
        userInfo = pattern3.findall(s3.text)
        j = json.loads(userInfo[0])
        for i in range(0, len(s1)):
            uid = pattern1.findall(s2[i]['href'])[0]
            id = pattern2.findall(s1[i].get('id'))[0]
            username = j[uid]['username']
            content = s1[i].text
            w.write(f'<p>{id}:{username}\t:{uid}:\t{content}</p>\n')
            #w.write(uid+":"+s1[i].text+"\n")
            print(id+','+uid+','+username+":"+s1[i].text+"\n")


name = "五年没见面的人   你还会梦见她吗？"
with open(f'{name}/{name}4.html', 'r', encoding='gbk') as f:
    get_content(f, name)
