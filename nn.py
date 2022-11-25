import requests
import asyncio
import time
import aiofiles

start=time.perf_counter()
async def write():
    r = requests.get("https://baidu.com")
    print(r.status_code)
    global start
    start=time.perf_counter()-start
    print('write_start:',time.perf_counter()-start)
    async with aiofiles.open('baidu.html','w') as f:
        await f.write(r.text)
    print('write_end:',time.perf_counter()-start)

async def main():
    t1=asyncio.create_task(write())
    t2=asyncio.create_task(finish())
    print('start:',time.perf_counter()-start)
    await t1
    print('write_next:', time.perf_counter()-start)
    await t2
    print('finish_next:', time.perf_counter()-start)

async def finish():
    print('finish:', time.perf_counter()-start)

asyncio.run(main())