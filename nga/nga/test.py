class Request:

    def __init__(self):
        self.session = None
        self.init_async()

    def init_async(self):
        asyncio.ensure_future(self.init_session())

    async def init_session(self):
        with open('nga.json', 'r', encoding='utf-8') as f:
            cookies = await self.mongo.read_cookies()
            self.session = aiohttp.ClientSession(cookies=cookies)
            return self.session
