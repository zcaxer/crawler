import re

strings = [
    "[quote][pid=678981876,35695802,1]Reply[/pid] [b]Post by [uid=64935241]等天依1130[/uid] (2023-03-17 23:30):[/b]没有秘密，也没有对象[/quote]看哭了()",
    "[quote][pid=679004858,35695802,2]Reply[/pid] [b]Post by [uid=-1]庚舒戚己邬罗[/uid][color=gray](30楼)[/color] (2023-03-18 04:04):[/b]<br/>虽然没试过别人的，但每次说他内个好大弄得我好痛都是装的。[s:a2:偷吃][/quote]<br/>之前谁说喊爽是装的，喊痛是真的觉得男方厉害的站出来[img]http://img4.nga.cn/ngabbs/post/smile/a2_28.png[/img]",
    "[quote][tid=35695802]Topic[/tid] [b]Post by [uid=62281165]LeDoory[/uid] (2023-03-17 23:27):[/b]送给老婆第一个礼物是前女友退还给我的[/quote]没有秘密 人生信息100%和老婆共享 无丝毫隐瞒 包括我喜欢看本论坛的COS区(全是大凶妹)",
    "[quote][pid=679767381,35695802,65]Reply[/pid] [b]Post by [uid]#anony_97c905d44e47955b660ee20809486f86[/uid][color=gray](1286楼)[/color] (2023-03-22 10:47):[/b]<br/><br/>[s:ac:哭笑]<br/>我喜欢大的，看着赏心悦目<br/>吃起来会很舒服[/quote]<br/><br/>多大算大啊[s:ac:哭笑]",
    "[quote][pid=680326502,35695802,91]Reply[/pid] [b]Post by [uid=21600289]海涛晚睡[/uid] (2023-03-25 09:12):[/b]<br/><br/>[quote][pid=679393300,35695802,32]Reply[/pid] [b]Post by [uid]#anony_97c905d44e47955b660ee20809486f86[[/quote]<br/><br/>这是什么[s:ac:晕]",
    "[b]Reply to [pid=679000126,35695802,2]Reply[/pid] Post by [uid]#anony_50280e1dd5e2e5a4a1b023dd98d2c345[/uid][color=gray](20楼)[/color] (2023-03-18 02:16)[/b]展开说说",
    "[b]Reply to [pid=679158755,35695802,12]Reply[/pid] Post by [uid=43315906]F_goye[/[s:ac:赞同]uid] (2023-03-19 01:10)[/b]羡慕是这样的女友",

]

p = re.compile(
    r"(\[quote\]|\[b\]).*\[[pt]id=(\d+).*?Post\s*by\s*\[uid=?(-?\d*)\](.*)\[/uid\].*\[/(?:b|quote)\](.*)$"
)

# We can iterate through the list of strings and apply the regex pattern to each string
for string in strings:
    match = p.search(string)
    if match:
        print(match.groups())
    else: print(f'failed:{string}')
