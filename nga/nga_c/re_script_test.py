import re

s = """ngaAds.bbs_ads8_load_new($('postsign2347').parentNode.nextSibling,2347,'-7955747')
commonui.postArg.proc( 2347,
$('postcontainer2347'),$('postsubject2347'),$('postcontent2347'),$('postsign2347'),$('posterinfo2347'),$('postInfo2347'),$('postBtnPos2347'),
null,null,681888072,0,
null,'43103063',1680444471,'0,1,0','-2',
'','','8 Android','',null,0 )
if(ngaAds.bbs_ads31_gen)ngaAds.bbs_ads31_gen('post1strow2347')
"""

pattern_script = re.compile(
    r"postBtnPos\d+'\),\s*null,null,(\d+),-?\d+,\s*null,'(-?\d+)',-?\d+,'\d+,(\d+),\d+','-?\d*'"
)
match=pattern_script.search(s)
if match:
    print(match.groups())
else:
    print('failed')