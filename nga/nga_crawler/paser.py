# content analyzer

"""deal with texts and pics"""

import logging
import re
from .fetcher import download_img

class_list = ['ac', 'a2', 'ng', 'pst', 'dt', 'pg']
l = [["smile", "mrgreen", "question", "wink", "redface", "sad", "crazy", "cool",
      '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'
      '20', '21', '22', '23'],
     ['blink', 'goodjob', '上', '中枪', '偷笑', '冷', '凌乱','吓', '吻', '呆', '咦', '哦', '哭', '哭1','哭笑',
     '喘', '心', '囧', '晕', '汗', '瞎', '羞', '羡慕','委屈', '忧伤', '怒', '怕', '惊', '愁', '抓狂','哼','喷',
        '嘲笑', '嘲笑1', '抠鼻', '无语', '衰', '黑枪', '花痴','闪光', '擦汗', '茶', '计划通', '反对', '赞同',],
     ['goodjob', '诶嘿', '偷笑', '怒', '笑', '那个…','哦嗬嗬嗬', '舔', '鬼脸', '冷', '大哭', '哭', '恨','中枪',
      '囧', '你看看你', 'doge', '自戳双目', '偷吃','冷笑', '壁咚', '不活了', '不明觉厉', '是在下输了',
      '你为猴这么', '干杯', '干杯2', '异议', '认真', '你已经死了','你这种人…', '妮可妮可妮', '惊', '抢镜头',
       'yes', '有何贵干','病娇', 'lucky', 'poi', '囧2', '威吓', 'jojo立', 'jojo立2','jojo立3', 'jojo立4', 
       'jojo立5',],
     ['呲牙笑', '奸笑', '问号', '茶', '笑指', '燃尽', '晕', '扇笑','寄', '别急', 'doge', '丧', '汗', '叹气', '吃饼', '吃瓜',
      '吐舌', '哭', '喘', '心', '喷', '困', '大哭', '大惊', '害怕','惊', '暴怒', '气愤', '热', '瓜不熟', '瞎', '色', '斜眼',
      '问号大',],
     ['举手', '亲', '偷笑', '偷笑2', '偷笑3', '傻眼', '傻眼2', '兔子', '发光', '呆', '呆2', '呆3', '呕', '呵欠',
         '哭', '哭2', '哭3', '嘲笑', '基', '宅', '安慰','幸福', '开心', '开心2', '开心3', '怀疑', '怒','怒2', '怨',
         '惊吓', '惊吓2', '惊呆', '惊呆2', '惊呆3','惨', '斜眼', '晕', '汗', '泪', '泪2', '泪3', '泪4','满足', '满足2',
          '火星', '牙疼', '电击', '看戏', '眼袋','眼镜', '笑而不语', '紧张', '美味', '背', '脸红', '脸红2',
      '腐', '星星眼', '谢', '醉', '闷', '闷2', '音乐', '黑脸','鼻血',],
     ['ROLL', '上', '傲娇', '叉出去', '发光', '呵欠', '哭', '啃古头','嘲笑', '心', '怒', '怒2', '怨', '惊', '惊2', '无语',
     '星星眼','星星眼2', '晕', '注意', '注意2', '泪', '泪2', '烧', '笑','笑2', '笑3', '脸红', '药', '衰', '鄙视', '闲',
      '黑脸',],
     ['战斗力', '哈啤', '满分', '衰', '拒绝', '心', '严肃', '吃瓜','嘣', '嘣2', '冻', '谢', '哭', '响指', '转身',]]



def repl(matchobj):
    pic_class = matchobj.group(1)
    pic_name = matchobj.group(2)
    if pic_class == '0':
        index = int(pic_name)
        pic_name = l[0][index]
        return f'<img src="../emoji/{pic_name}.gif>'
    if pic_class in class_list:
        class_index = class_list.index(pic_class)+1
        if pic_name in l[class_index]:
            pic_number = l[class_index].index(pic_name)
            if pic_class=='pst':
                pic_class='pt'
            if pic_class in ('ng', 'a2'):
                pic_class = pic_class+'_'
            if pic_number<10:
                pic_class=pic_class+'0'
            return f'<img src="../emoji/{pic_class}{pic_number}.png">'
    return f'[s:{pic_class}:{pic_name}]'


def emoji_paser(content):
    pattern = re.compile(r'\[s:(.+?):(.+?)\]')
    match = pattern.search(content)
    if match:
        return pattern.sub(repl, content)
    return content


def img_parser(session,title, post_content: str):
    # logging.info(f'Processing {self.title} img url')
    # logging.info(f'Processing {self.title} img url')
    pattern_img = re.compile(r'(.*?)\[img\]\.?(.+?)\[/img\](.*?)')
    match_img = pattern_img.findall(post_content)
    if not match_img:
        return post_content
    pattern_pic_name = re.compile(r'.*/(.*?\..*?)$')
    post_content = ''
    for i in match_img:
        pic_name = pattern_pic_name.search(i[1]).group(1)
        download_img(session, i[1], title, pic_name)
        post_content += f'{i[0]}<img src="../htmls/{title}/img/{pic_name}">{i[2]}'
    return post_content


def reply_paser(original_post_content):
    logging.info('开始处理引用和回复')
    post_content = ''
    pattern_quote = re.compile(
        r'\[b\]\s*Post\s*by\s*\[uid=?\d*\](.*)\[/uid\].*\(.*\):\[/b\](.*)\[\/quote\](.*)')
    match_quote = pattern_quote.search(original_post_content)
    if match_quote:
        logging.debug('引用')
        quote_uname = match_quote.groups()[0]
        quote_content = match_quote.groups()[1]
        reply_content = match_quote.groups()[2]
        post_content += f'<blockquote><p>{quote_uname}:{quote_content}</p></blockquote>{reply_content}'
        return post_content
    pattern_reply = re.compile(
        r'\[b\]Reply to \[pid=\d+,\d+,\d+\]Reply\[/pid\] Post by \[uid=?\d*\](.*)\[/uid\] \((.*)\)\[/b\](.*)')
    match_reply = pattern_reply.search(original_post_content)
    if match_reply:
        logging.debug('回复')
        post_uname = match_reply.groups()[0]
        post_time = match_reply.groups()[1]
        reply_content = match_reply.groups()[2]
        # print(post_uname, post_time)
        pattern_post_content = re.compile(
            rf'<p>\d+:{post_uname},{post_time},\d+,up:\d+:<br>(.*)\n?</p>\s')
        original_post_content = '未匹配到'
        match = pattern_post_content.search(nga.result_html)
        if match:
            original_post_content = match.group(1)
        post_content += f'<blockquote><p>{post_uname}:{original_post_content}</p></blockquote>{reply_content}'
        return post_content
    return original_post_content
