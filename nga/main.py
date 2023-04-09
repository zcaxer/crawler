import logging
import asyncio
import argparse
import json

from nga.main import Nga_clawler
from nga.nga import Nga

async def read_htmls():
    with open('nga/nga.json','r') as json_file:
        data = json.load(json_file) 
    info=data['finished_ids']
    crawler=Nga_clawler()
    for key in info:
        topic=Nga.Topic(key,title=info[key]['title'])
        crawler.topics.append(topic)
        await crawler.start(topic)

   
logging.basicConfig(level=logging.DEBUG)
arg_parser = argparse.ArgumentParser(description="nga 爬虫")
arg_parser.add_argument(
    '-u', '--update', action='store_true', help='更新爬虫库中的帖子')
arg_parser.add_argument(
    '-f', '--force', action='store_true', help='强制更新该id的帖子')
arg_parser.add_argument('id', metavar='ID', nargs='*', type=int)
args = arg_parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

async def main():
    args.update=1
    if args.update:
        crawler=Nga_clawler()
        await crawler.update()
    print(args)
    #nga_clawler = Nga_clawler(args.id)


    #await read_htmls()

asyncio.run(main())
