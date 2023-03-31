import logging
import asyncio
from nga.main import Nga_clawler
import argparse
from nga.nga import Topic

logging.basicConfig(level=logging.DEBUG)
arg_parser = argparse.ArgumentParser(description="nga 爬虫")
arg_parser.add_argument(
    '-u', '--update', action='store_true', help='更新爬虫库中的帖子')
arg_parser.add_argument(
    '-f', '--force', action='store_true', help='强制更新该id的帖子')
arg_parser.add_argument('id', metavar='ID', nargs='*', type=int)
args = arg_parser.parse_args()


async def main():
    #if args.update:
        #nga_clawler.update()
    print(args)
    #nga_clawler = Nga_clawler(args.id)
    nga_clawler= Nga_clawler([35818299])
    for topic in nga_clawler.topics:
        topic.state = await nga_clawler.start(topic)

asyncio.run(main())
