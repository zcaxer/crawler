import logging
import asyncio
import argparse
import json

from nga.main import Nga_clawler
from nga.nga import Nga

async def read_htmls():
    with open('nga/nga.json','r') as json_file:
        data = json.load(json_file) 
    info1=data['finished_ids']
    info2=data['ongoing_ids']
    crawler=Nga_clawler()
    info= info1 | info2

    for key in info:
        topic=Nga.Topic(key,title=info[key]['title'])
        await crawler.start(topic)

   
logging.basicConfig(level=logging.DEBUG)
arg_parser = argparse.ArgumentParser(description="nga 爬虫")
arg_parser.add_argument(
    '-u', '--update', action='store_true', help='更新爬虫库中的帖子')
arg_parser.add_argument(
    '-f', '--force', action='store_true', help='强制更新不活跃帖子')
arg_parser.add_argument(
    '-d','--delete', metavar='DELETE',type=str,nargs='*',help='删除title包含str的帖子'
)
arg_parser.add_argument('id', metavar='ID', nargs='*', type=int)

args = arg_parser.parse_args()
#args.update=1
logging.basicConfig(level=logging.DEBUG)

async def main():
    crawler=Nga_clawler()
    if args.delete:
        for key_str in args.delete:
            await crawler.delete_topic(key_str)

    if args.update:
        await crawler.update_all()
    print(args)

    if args.force:
        await crawler.update_all(True)
#1
#     args.id=[36004549]
    for tid in args.id:
        await crawler.start(Nga.Topic(tid))

    #await read_htmls()

    await crawler.get_index()
  
    await crawler.request.session.close()

asyncio.run(main())
