import requests
from nga.mongo import Mongo

mongo=Mongo()
cookies=mongo.read_cookies()

session = requests.Session()
session.cookies.update(cookies)

r=session.get('https://nga.178.com/read.php?tid=35695802')
print(r.text)
