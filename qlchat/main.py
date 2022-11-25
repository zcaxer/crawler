
from playwright.sync_api import Playwright, sync_playwright, expect,Page
import json
import re
import time

cookies = []
with open('auth.json', 'r') as f:
    j = json.load(f)
    cookies = j.get('cookies')
# cookies = [{'name': 'uid', 'value': 'ddd52447-40674bb2-9df2a0fb-e5e65f3b%3D1669035124898%3D1700571124898',
# 'domain': 'm.qlchat.com', 'path': '/', 'expires': 1669639924, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}, {'name': 'sid', 'value': '156fd62d-e49e4d3d-9867c3fc-29272755%3D1669035124898', 'domain': 'm.qlchat.com',                                                                                                                                               'path': '/', 'expires': 1669639924, 'httpOnly': False, 'secure': False, 'sameSite': 'Lax'}, {'name': 'rsessionid', 'value': 'qlwrsid%3A3C8514F9-7DC8-4C3F-AB8D-70D8A9FF6E23.1aCKexANgIB26jbkqV9ek9fVetqhpjrB%2FX5AcMSzlAI', 'domain': 'm.qlchat.com', 'path': '/', 'expires': -1, 'httpOnly': True, 'secure': False, 'sameSite': 'Lax'}]
url = "https://m.qlchat.com/wechat/page/channel-intro?channelId=2000013397272766&"

def scroll_to_end(page:Page,keyword):
    a = 0
    while a == 0:
        page.mouse.wheel(0,2000)
        page.keyboard.down("PageDown")
        try:
                page.wait_for_selector(f"text={keyword}", timeout=500, state='attached')
                a = 1
        except:
                a = 0

def run(playwright: Playwright) -> None:
    #browser = playwright.chromium.launch(headless=False)
    browser = playwright.chromium.launch()
    context = browser.new_context(viewport={'width':640,'height':640})
    #context = browser.new_context(**playwright.devices["iPhone 13 Pro Max"])
    context.add_cookies(cookies)
    context.set_default_timeout(0)
    page = context.new_page()
    page.goto(url)
    page.locator(".title").first.click()
    scroll_to_end(page,"没有更多了")
    #page.pause()
    p=re.compile("video")
    titles=page.locator("[class='title elli-text']")
    for i in range(titles.count()):
        page.locator(".title").first.click()
        scroll_to_end(page,"没有更多了")
        titles.nth(i).click()
        if p.search(page.url):
            page.goto(url)
            break
        page.locator("text=听课指南").first.click()
        scroll_to_end(page,"直播结束")
        page.wait_for_timeout(5000)
        with open(f'{page.title()}.html','w') as f:
            f.write(page.content())
        
        names = page.locator("[class='doc-name elli-text']").all_text_contents()
        downloads=page.locator('text=立即下载')
        url_lesson=page.url
        for j in range(downloads.count()):
            page.locator("text=听课指南").first.click()
            scroll_to_end(page, "直播结束")
            downloads.nth(j).click(timeout=0)
            #page.pause()
            a=1
            while a:
                try:
                    with page.expect_download(timeout=1000) as d_info:
                        page.mouse.click(520,25,button="left")
                    a=0
                except:
                    a=1    
            d=d_info.value
            print(d.path())
            d.save_as(names[j])
            page.goto(url_lesson)
        page.goto(url)
       
    j["cookies"]= context.cookies(url)
    with open('auth.json', 'w') as f:
        json.dump(j, f)

    #page.get_by_text("012021年3月3周甄选研报（可试看）").click()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
