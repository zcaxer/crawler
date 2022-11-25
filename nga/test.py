import asyncio
import time


async def say(id):
    print(f'{id}:1')
    await asyncio.sleep(3)
    print(f'{id}:2')

async def main():
    print('start')
#   await say(1)
#    await say(2)
    await asyncio.gather(say(1),say(2))
    print('finish')

asyncio.run(main())
print(3)
