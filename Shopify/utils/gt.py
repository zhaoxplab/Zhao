import asyncio
import aiohttp
import json
import re
from fake_useragent import UserAgent
ua = UserAgent()


class GetTheme(object):
    def __init__(self, urls):
        self.session = None
        self.urls = urls  # 是个列表啊，['url_1', 'url_2', 'url3']
        self.result = []
        self.head = {
            'headers': ua.random
        }
        pass

    # 2.获取响应
    async def resp(self, u):
        async with self.session.get(u) as response:
            return await response.text()

    """
    # 解析
    async def parse(self, h):
        info = re.findall(r'Shopify.theme = ([\s\S]*?);', h)
        theme = json.loads(info[0])['name']
        print(theme)
    """

    # 1.生成任务
    async def main(self, url):
        # async with concurrent:
        async with aiohttp.ClientSession() as self.session:
            html = await self.resp(url)
            # await self.parse(html)
            info = re.findall(r'Shopify.theme = ([\s\S]*?);', html)  # 3.解析主题模板信息
            theme = json.loads(info[0])['name']
            x = dict({'link': url, 'theme': theme})
            self.result.append(x)

    def run(self):
        # semaphore = asyncio.Semaphore(64)  # 限制并发数，把这个打开会引发
        # RuntimeError: There is no current event loop in thread 'Thread-2'.
        # 为了解决上边的问题
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(self.main(url)) for url in self.urls]  # 把url加入任务列表
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)
        # 返回一个列表
        return self.result
