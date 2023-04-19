# content analyzer

"""deal with texts and pics"""

import logging
import re
import json
from datetime import datetime
from .nga import Nga
from .mongo import Mongo

mongo = Mongo()

emoji_dict = {
    "0": {
        "1": "smile.gif",
        "2": "mrgreen.gif",
        "3": "question.gif",
        "4": "wink.gif",
        "5": "redface.gif",
        "6": "sad.gif",
        "7": "cool.gif",
        "8": "crazy.gif",
        "24": "04.gif",
        "25": "05.gif",
        "26": "06.gif",
        "27": "07.gif",
        "28": "08.gif",
        "29": "09.gif",
        "30": "10.gif",
        "32": "12.gif",
        "33": "13.gif",
        "34": "14.gif",
        "35": "15.gif",
        "36": "16.gif",
        "37": "17.gif",
        "38": "18.gif",
        "39": "19.gif",
        "40": "20.gif",
        "41": "21.gif",
        "42": "22.gif",
        "43": "23.gif",
    },
    "ac": {
        "blink": "ac0.png",
        "goodjob": "ac1.png",
        "上": "ac2.png",
        "中枪": "ac3.png",
        "偷笑": "ac4.png",
        "冷": "ac5.png",
        "凌乱": "ac6.png",
        "吓": "ac8.png",
        "吻": "ac9.png",
        "呆": "ac10.png",
        "咦": "ac11.png",
        "哦": "ac12.png",
        "哭": "ac13.png",
        "哭1": "ac14.png",
        "哭笑": "ac15.png",
        "喘": "ac17.png",
        "心": "ac23.png",
        "囧": "ac21.png",
        "晕": "ac33.png",
        "汗": "ac34.png",
        "瞎": "ac35.png",
        "羞": "ac36.png",
        "羡慕": "ac37.png",
        "委屈": "ac22.png",
        "忧伤": "ac24.png",
        "怒": "ac25.png",
        "怕": "ac26.png",
        "惊": "ac27.png",
        "愁": "ac28.png",
        "抓狂": "ac29.png",
        "哼": "ac16.png",
        "喷": "ac18.png",
        "嘲笑": "ac19.png",
        "嘲笑1": "ac20.png",
        "抠鼻": "ac30.png",
        "无语": "ac32.png",
        "衰": "ac40.png",
        "黑枪": "ac44.png",
        "花痴": "ac38.png",
        "闪光": "ac43.png",
        "擦汗": "ac31.png",
        "茶": "ac39.png",
        "计划通": "ac41.png",
        "反对": "ac7.png",
        "赞同": "ac42.png"
    },
    "a2": {
        "goodjob": "a2_02.png",
        "诶嘿": "a2_05.png",
        "偷笑": "a2_03.png",
        "怒": "a2_04.png",
        "笑": "a2_07.png",
        "那个…": "a2_08.png",
        "哦嗬嗬嗬": "a2_09.png",
        "舔": "a2_10.png",
        "鬼脸": "a2_14.png",
        "冷": "a2_16.png",
        "大哭": "a2_15.png",
        "哭": "a2_17.png",
        "恨": "a2_21.png",
        "中枪": "a2_23.png",
        "囧": "a2_24.png",
        "你看看你": "a2_25.png",
        "doge": "a2_27.png",
        "自戳双目": "a2_28.png",
        "偷吃": "a2_30.png",
        "冷笑": "a2_31.png",
        "壁咚": "a2_32.png",
        "不活了": "a2_33.png",
        "不明觉厉": "a2_36.png",
        "是在下输了": "a2_51.png",
        "你为猴这么": "a2_53.png",
        "干杯": "a2_54.png",
        "干杯2": "a2_55.png",
        "异议": "a2_47.png",
        "认真": "a2_48.png",
        "你已经死了": "a2_45.png",
        "你这种人…": "a2_49.png",
        "妮可妮可妮": "a2_18.png",
        "惊": "a2_19.png",
        "抢镜头": "a2_52.png",
        "yes": "a2_26.png",
        "有何贵干": "a2_11.png",
        "病娇": "a2_12.png",
        "lucky": "a2_13.png",
        "poi": "a2_20.png",
        "囧2": "a2_22.png",
        "威吓": "a2_42.png",
        "jojo立": "a2_37.png",
        "jojo立2": "a2_38.png",
        "jojo立3": "a2_39.png",
        "jojo立4": "a2_41.png",
        "jojo立5": "a2_40.png"
    },
    "ng": {
        "呲牙笑": "ng_1.png",
        "奸笑": "ng_2.png",
        "问号": "ng_3.png",
        "茶": "ng_4.png",
        "笑指": "ng_5.png",
        "燃尽": "ng_6.png",
        "晕": "ng_7.png",
        "扇笑": "ng_8.png",
        "寄": "ng_9.png",
        "别急": "ng_10.png",
        "doge": "ng_11.png",
        "丧": "ng_12.png",
        "汗": "ng_13.png",
        "叹气": "ng_15.png",
        "吃饼": "ng_16.png",
        "吃瓜": "ng_17.png",
        "吐舌": "ng_18.png",
        "哭": "ng_19.png",
        "喘": "ng_20.png",
        "心": "ng_21.png",
        "喷": "ng_22.png",
        "困": "ng_24.png",
        "大哭": "ng_25.png",
        "大惊": "ng_26.png",
        "害怕": "ng_27.png",
        "惊": "ng_28.png",
        "暴怒": "ng_30.png",
        "气愤": "ng_31.png",
        "热": "ng_32.png",
        "瓜不熟": "ng_33.png",
        "瞎": "ng_34.png",
        "色": "ng_35.png",
        "斜眼": "ng_37.png",
        "问号大": "ng_38.png"
    },
    "pst": {
        "举手": "pt00.png",
        "亲": "pt01.png",
        "偷笑": "pt02.png",
        "偷笑2": "pt03.png",
        "偷笑3": "pt04.png",
        "傻眼": "pt05.png",
        "傻眼2": "pt06.png",
        "兔子": "pt07.png",
        "发光": "pt08.png",
        "呆": "pt09.png",
        "呆2": "pt10.png",
        "呆3": "pt11.png",
        "呕": "pt12.png",
        "呵欠": "pt13.png",
        "哭": "pt14.png",
        "哭2": "pt15.png",
        "哭3": "pt16.png",
        "嘲笑": "pt17.png",
        "基": "pt18.png",
        "宅": "pt19.png",
        "安慰": "pt20.png",
        "幸福": "pt21.png",
        "开心": "pt22.png",
        "开心2": "pt23.png",
        "开心3": "pt24.png",
        "怀疑": "pt25.png",
        "怒": "pt26.png",
        "怒2": "pt27.png",
        "怨": "pt28.png",
        "惊吓": "pt29.png",
        "惊吓2": "pt30.png",
        "惊呆": "pt31.png",
        "惊呆2": "pt32.png",
        "惊呆3": "pt33.png",
        "惨": "pt34.png",
        "斜眼": "pt35.png",
        "晕": "pt36.png",
        "汗": "pt37.png",
        "泪": "pt38.png",
        "泪2": "pt39.png",
        "泪3": "pt40.png",
        "泪4": "pt41.png",
        "满足": "pt42.png",
        "满足2": "pt43.png",
        "火星": "pt44.png",
        "牙疼": "pt45.png",
        "电击": "pt46.png",
        "看戏": "pt47.png",
        "眼袋": "pt48.png",
        "眼镜": "pt49.png",
        "笑而不语": "pt50.png",
        "紧张": "pt51.png",
        "美味": "pt52.png",
        "背": "pt53.png",
        "脸红": "pt54.png",
        "脸红2": "pt55.png",
        "腐": "pt56.png",
        "星星眼": "pt57.png",
        "谢": "pt58.png",
        "醉": "pt59.png",
        "闷": "pt60.png",
        "闷2": "pt61.png",
        "音乐": "pt62.png",
        "黑脸": "pt63.png",
        "鼻血": "pt64.png"
    },
    "dt": {
        "ROLL": "dt01.png",
        "上": "dt02.png",
        "傲娇": "dt03.png",
        "叉出去": "dt04.png",
        "发光": "dt05.png",
        "呵欠": "dt06.png",
        "哭": "dt07.png",
        "啃古头": "dt08.png",
        "嘲笑": "dt09.png",
        "心": "dt10.png",
        "怒": "dt11.png",
        "怒2": "dt12.png",
        "怨": "dt13.png",
        "惊": "dt14.png",
        "惊2": "dt15.png",
        "无语": "dt16.png",
        "星星眼": "dt17.png",
        "星星眼2": "dt18.png",
        "晕": "dt19.png",
        "注意": "dt20.png",
        "注意2": "dt21.png",
        "泪": "dt22.png",
        "泪2": "dt23.png",
        "烧": "dt24.png",
        "笑": "dt25.png",
        "笑2": "dt26.png",
        "笑3": "dt27.png",
        "脸红": "dt28.png",
        "药": "dt29.png",
        "衰": "dt30.png",
        "鄙视": "dt31.png",
        "闲": "dt32.png",
        "黑脸": "dt33.png"
    },
    "pg": {
        "战斗力": "pg01.png",
        "哈啤": "pg02.png",
        "满分": "pg03.png",
        "衰": "pg04.png",
        "拒绝": "pg05.png",
        "心": "pg06.png",
        "严肃": "pg07.png",
        "吃瓜": "pg08.png",
        "嘣": "pg09.png",
        "嘣2": "pg10.png",
        "冻": "pg11.png",
        "谢": "pg12.png",
        "哭": "pg13.png",
        "响指": "pg14.png",
        "转身": "pg15.png"
    }
}


class Parser:

    @staticmethod
    def _repl(matchobj):
        emoji_class = matchobj.group(1)
        emoji_code = matchobj.group(2)
        if emoji_class == "":
            emoji_class='0'
        try:
            emoji_pic_name=emoji_dict[emoji_class][emoji_code]
            return f'<img src="../emoji/{emoji_pic_name}">'
        except:
            logging.error(f'{emoji_class}:{emoji_code} not found')
            return f"[s:{emoji_class}:{emoji_code}]"

    @staticmethod
    async def emoji_parser(content):
        pattern = re.compile(r"\[s:(.*?):(.+?)\]")
        match = pattern.search(content)
        if match:
            return pattern.sub(Parser._repl, content)
        return content

    @staticmethod
    async def img_parser(request,topic_title, post_content: str):
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
            await request.download_img(i[1], topic_title, pic_name)
            post_content += (
                f'{i[0]}<img src="../htmls/{topic_title}/img/{pic_name}">{i[2]}'
            )
        return post_content

    @staticmethod
    async def comment_parser(post: Nga.Post, topic: Nga.Topic):
        #logging.info("开始处理引用和回复")
        parsed_html = ""
        pattern_comment = re.compile(
            r"(\[quote\]|\[b\]).*\[[pt]id=(\d+).*?Post\s*by\s*\[uid=?(-?\d*)\](.*)\[/uid\].*\[/(?:b|quote)\](.*?)$"
        )
        match_comment = pattern_comment.search(post.content)
        if match_comment:
            info_list = match_comment.groups()
            comment_type = info_list[0]
            commented_pid = int(info_list[1])
            commented_uid_str = info_list[2]
            commented_post = await topic.search_post(commented_pid)
            post.content = info_list[4]
            if commented_post is not None:
                if commented_uid_str == "":
                    # commented_uid = commented_uid_str  # 匿名
                    commented_uname = commented_post.author_name
                else:
                    # commented_uid = int(commented_uid_str)
                    commented_uname = info_list[3]
                if comment_type == "[quote]":
                    comment_type = "引用"
                    commented_post.quoted_by.append(post.index)
                    post.quote_to = commented_post.index

                elif comment_type == "[b]":
                    comment_type = "回复"
                    commented_post.replied_by.append(post.index)
                    post.reply_to = commented_post.index

                logging.debug("%d楼检测到%s", post.index, comment_type)
                parsed_html += f"<blockquote><p>{commented_uname}:{commented_post.content}</p></blockquote>{post.content}"
                return parsed_html
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
    async def page_parser(request, soup, page_number, topic: Nga.Topic):
        logging.debug("开始解析第%d页", page_number)
        if topic.title is None:
            topic.title = Parser.get_title(soup)
        post_infos = soup.find_all("td", class_="c2")
        pattern_number = re.compile(r"\d+")
        pattern_user_info = re.compile(
            r"commonui\.userInfo\.setAll\(\s+(.*)\)")
        pattern_script = re.compile(
            r"postBtnPos\d+'\),\s*null,null,(\d+),-?\d+,\s*null,'(-?\d+)',-?\d+,'\d+,(\d+),\d+','-?\d*'"
        )
        # str_author_uid = soup.find_all(id=re.compile(r"postauthor\d+"))
        str_user_infos = soup.find(
            "script", {"type": "text/javascript"}, text=pattern_user_info
        )
        user_infos = pattern_user_info.findall(str_user_infos.string)
        user_info_json = json.loads(user_infos[0], strict=False)
        result_html = ""
        for post_info in post_infos:
            post_index_str = post_info["id"]
            post_index = int(pattern_number.search(post_index_str).group())
            post = Nga.Post(post_index)
            post_script_str = post_info.parent.parent.next_sibling.text
            try:
                info_list = pattern_script.search(post_script_str).groups()
            except:
                logging.error("正则错误：%s", post_script_str)
            post.pid = int(info_list[0])
            if post.pid==0:post.pid=topic.tid
            post.author_id = int(info_list[1])
            post.up_count = int(info_list[2])
            if str(post.author_id) in user_info_json:
                post.author_name = user_info_json[str(
                    post.author_id)]["username"]
            else:
                logging.error("%s获取用户名失败", post.author_id)
            if post.author_id < 0:
                # 匿名用户,id为 userInfo 中的username,author_name为匿名+第几个出现的匿名poster
                post.author_id = post.author_name
                if post.author_id in topic.anony_posters:
                    post.author_name = f'匿名{topic.anony_posters.index(post.author_id)}'
                else:
                    topic.anony_posters.append(post.author_id)
                    post.author_name = f"匿名{len(topic.anony_posters)}"
            date_string = post_info.span.text
            post.date = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
            post.content = post_info.find(
                ["span", "p"], class_="postcontent").text
            post.content = await Parser.img_parser(request,topic.title, post.content)
            post.content = await Parser.emoji_parser(post.content)
            parsed_html = await Parser.comment_parser(post, topic)
            result_html = (
                result_html
                + f"<p>{post.index}:{post.author_name},{post.author_id},{post.date},up:{post.up_count}:<br>{parsed_html}</p>\n"
            )
            topic.add_post(post, True)
        logging.info("第%d页解析完成", page_number)
        return result_html
