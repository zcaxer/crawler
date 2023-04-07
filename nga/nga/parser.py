# content analyzer

"""deal with texts and pics"""

import logging
import re
import json
from datetime import datetime
from .request import Request
from .nga import Nga
from .mongo import Mongo

mongo = Mongo()

emoji_class_list = ["ac", "a2", "ng", "pst", "dt", "pg"]
emoji_list = [
    [
        "smile",
        "mrgreen",
        "question",
        "wink",
        "redface",
        "sad",
        "crazy",
        "cool",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
    ],
    [
        "blink",
        "goodjob",
        "上",
        "中枪",
        "偷笑",
        "冷",
        "凌乱",
        "吓",
        "吻",
        "呆",
        "咦",
        "哦",
        "哭",
        "哭1",
        "哭笑",
        "喘",
        "心",
        "囧",
        "晕",
        "汗",
        "瞎",
        "羞",
        "羡慕",
        "委屈",
        "忧伤",
        "怒",
        "怕",
        "惊",
        "愁",
        "抓狂",
        "哼",
        "喷",
        "嘲笑",
        "嘲笑1",
        "抠鼻",
        "无语",
        "衰",
        "黑枪",
        "花痴",
        "闪光",
        "擦汗",
        "茶",
        "计划通",
        "反对",
        "赞同",
    ],
    [
        "goodjob",
        "诶嘿",
        "偷笑",
        "怒",
        "笑",
        "那个…",
        "哦嗬嗬嗬",
        "舔",
        "鬼脸",
        "冷",
        "大哭",
        "哭",
        "恨",
        "中枪",
        "囧",
        "你看看你",
        "doge",
        "自戳双目",
        "偷吃",
        "冷笑",
        "壁咚",
        "不活了",
        "不明觉厉",
        "是在下输了",
        "你为猴这么",
        "干杯",
        "干杯2",
        "异议",
        "认真",
        "你已经死了",
        "你这种人…",
        "妮可妮可妮",
        "惊",
        "抢镜头",
        "yes",
        "有何贵干",
        "病娇",
        "lucky",
        "poi",
        "囧2",
        "威吓",
        "jojo立",
        "jojo立2",
        "jojo立3",
        "jojo立4",
        "jojo立5",
    ],
    [
        "呲牙笑",
        "奸笑",
        "问号",
        "茶",
        "笑指",
        "燃尽",
        "晕",
        "扇笑",
        "寄",
        "别急",
        "doge",
        "丧",
        "汗",
        "叹气",
        "吃饼",
        "吃瓜",
        "吐舌",
        "哭",
        "喘",
        "心",
        "喷",
        "困",
        "大哭",
        "大惊",
        "害怕",
        "惊",
        "暴怒",
        "气愤",
        "热",
        "瓜不熟",
        "瞎",
        "色",
        "斜眼",
        "问号大",
    ],
    [
        "举手",
        "亲",
        "偷笑",
        "偷笑2",
        "偷笑3",
        "傻眼",
        "傻眼2",
        "兔子",
        "发光",
        "呆",
        "呆2",
        "呆3",
        "呕",
        "呵欠",
        "哭",
        "哭2",
        "哭3",
        "嘲笑",
        "基",
        "宅",
        "安慰",
        "幸福",
        "开心",
        "开心2",
        "开心3",
        "怀疑",
        "怒",
        "怒2",
        "怨",
        "惊吓",
        "惊吓2",
        "惊呆",
        "惊呆2",
        "惊呆3",
        "惨",
        "斜眼",
        "晕",
        "汗",
        "泪",
        "泪2",
        "泪3",
        "泪4",
        "满足",
        "满足2",
        "火星",
        "牙疼",
        "电击",
        "看戏",
        "眼袋",
        "眼镜",
        "笑而不语",
        "紧张",
        "美味",
        "背",
        "脸红",
        "脸红2",
        "腐",
        "星星眼",
        "谢",
        "醉",
        "闷",
        "闷2",
        "音乐",
        "黑脸",
        "鼻血",
    ],
    [
        "ROLL",
        "上",
        "傲娇",
        "叉出去",
        "发光",
        "呵欠",
        "哭",
        "啃古头",
        "嘲笑",
        "心",
        "怒",
        "怒2",
        "怨",
        "惊",
        "惊2",
        "无语",
        "星星眼",
        "星星眼2",
        "晕",
        "注意",
        "注意2",
        "泪",
        "泪2",
        "烧",
        "笑",
        "笑2",
        "笑3",
        "脸红",
        "药",
        "衰",
        "鄙视",
        "闲",
        "黑脸",
    ],
    [
        "战斗力",
        "哈啤",
        "满分",
        "衰",
        "拒绝",
        "心",
        "严肃",
        "吃瓜",
        "嘣",
        "嘣2",
        "冻",
        "谢",
        "哭",
        "响指",
        "转身",
    ],
]


class Parser:
    @staticmethod
    def _repl(matchobj):
        pic_class = matchobj.group(1)
        pic_name = matchobj.group(2)
        if pic_class == "0":
            index = int(pic_name)
            pic_name = emoji_list[0][index]
            return f'<img src="../emoji/{pic_name}.gif>'
        if pic_class in emoji_class_list:
            class_index = emoji_class_list.index(pic_class) + 1
            if pic_name in emoji_list[class_index]:
                pic_number = emoji_list[class_index].index(pic_name)
                if pic_class == "pst":
                    pic_class = "pt"
                if pic_class in ("ng", "a2"):
                    pic_class = pic_class + "_"
                if pic_number < 10:
                    pic_class = pic_class + "0"
                return f'<img src="../emoji/{pic_class}{pic_number}.png">'
        return f"[s:{pic_class}:{pic_name}]"

    @staticmethod
    async def emoji_parser(content):
        pattern = re.compile(r"\[s:(.+?):(.+?)\]")
        match = pattern.search(content)
        if match:
            return pattern.sub(Parser._repl, content)
        return content

    @staticmethod
    async def img_parser(topic_title, post_content: str):
        # logging.info(f'Processing {self.title} img url')
        # logging.info(f'Processing {self.title} img url')
        pattern_img = re.compile(r"(.*?)\[img\]\.?(.+?)\[/img\](.*?)")
        match_img = pattern_img.findall(post_content)
        if not match_img:
            return post_content
        pattern_pic_name = re.compile(r".*/(.*?\..*?)$")
        post_content = ""
        for i in match_img:
            pic_name = pattern_pic_name.search(i[1]).group(1)
            request = Request()
            await request.download_img(i[1], topic_title, pic_name)
            post_content += (
                f'{i[0]}<img src="../htmls/{topic_title}/img/{pic_name}">{i[2]}'
            )
        return post_content

    @staticmethod
    async def comment_parser(post:Nga.Post, topic:Nga.Topic):
        logging.info("开始处理引用和回复")
        post_html = ""
        pattern_comment = re.compile(
            r"(\[quote\]|\[b\]).*\[pid=(\d+),.*? Post\s*by\s*\[uid=?(\d*)\](.*)\[/uid\].*\[\w+\](.*)$"
        )
        match_comment = pattern_comment.search(post.content)
        if match_comment:
            info_list = match_comment.groups()
            comment_type=info_list[0]
            if comment_type == "[quote]":
                comment_type='引用'
            elif comment_type == "[b]":
                comment_type = '回复'
            logging.debug("%d楼检测到%s", post.index, comment_type)
            commented_pid = int(info_list[1])
            commented_uid_str = info_list[2]
            commented_post = await topic.search_post(commented_pid)
            if commented_uid_str == "":
                #commented_uid = 0  # 匿名
                commented_uname = commented_post.author_name
            else:
                #commented_uid = int(commented_uid_str)
                commented_uname = info_list[3]
            post.content = info_list[4]

            if commented_post is not None:
                topic.posts[commented_pid].replied_by.append(post.index)
                post.reply_to.append(commented_pid)
                replied_post_content = topic.posts[commented_pid].content
                post_html += f"<blockquote><p>{commented_uname}:{replied_post_content}</p></blockquote>{post.content}"
        return post.content
     
    @staticmethod
    async def get_title(soup):
        logging.info("开始解析标题")
        l1 = soup.find("title").text
        pattern1 = re.compile(r"(.*)\s178")
        title = pattern1.findall(l1)[0]
        title = str.replace(title, r"/", "-")
        logging.info("标题解析完成,title:%s", title)
        return title

    @staticmethod
    async def get_page_count(soup):
        try:
            l = soup.find(id="pageBtnHere").next_sibling.string
            pattern2 = re.compile(r",1:(\d+)")
            last_page = int(pattern2.findall(l)[0])
        except:
            last_page = 1
        logging.info("标题最大页数完成,%d", last_page)
        return last_page

    @staticmethod
    async def page_parser(soup, page, topic: Nga.Topic):
        logging.debug("开始解析第%d页", page)
        if topic.title is None:
            topic.title = Parser.get_title(soup)
        post_infos = soup.find_all("table", class_="c2")
        pattern_number = re.compile(r"\d+")
        pattern_user_info = re.compile(r"commonui\.userInfo\.setAll\(\s+(.*)\)")
        pattern_script = re.compile(
            r"postBtnPos\d+'\),\nnull,null,(\d+),-?\d+,\nnull,'(-?\d+)',-?\d+,'\d+,(\d+),\d+','\d+'"
        )
        #str_author_uid = soup.find_all(id=re.compile(r"postauthor\d+"))
        str_user_infos = soup.find(
            "script", {"type": "text/javascript"}, text=pattern_user_info
        )
        user_infos = pattern_user_info.findall(str_user_infos.string)
        user_info_json = json.loads(user_infos[0], strict=False)
        result_html = ""
        for post_info in post_infos:
            post_index_str = post_info["id"]
            post_index = int(pattern_number.search(post_index_str))
            post = Nga.Post(post_index)
            post_script_str = post_info.parent.parent.next_sibling.text
            try:
                info_list = pattern_script.search(post_script_str).groups()
            except:
                logging.error("正则错误：%s", post_script_str)
            post.pid = int(info_list[0])
            post.author_id = int(info_list[1])
            post.up_count = int(info_list[2])
            if str(post.author_id) in user_info_json:
                post.author_name = user_info_json[str(post.author_id)]["username"]
            elif post.author_id < 0:
                post.author_name = f"匿名{-1*post.author_id}"  # 匿名用户从 -1开始,每位减1
            else:
                logging.error("%s获取用户名失败", post.author_id)
            date_string = post_info.span.text
            post.date = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
            post.content = post_info.find("span", class_="postcontent").text
            post.content = await Parser.img_parser(topic.title, post.content)
            post.content = await Parser.comment_parser(post, topic)
            result_html = (
                result_html
                + f"<p>{post.index}:{post.author_name},{post.date},{post.author_id},up:{post.up_count}:<br>{post.content}</p>\n"
            )
            topic.add_post(post,True)
        logging.info("第%d页解析完成", page)
        return result_html
