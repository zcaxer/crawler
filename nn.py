import requests

r = requests.get("https://baidu.com")
print(r.status_code)
