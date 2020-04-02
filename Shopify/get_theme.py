import asyncio
import aiohttp
import json
import time
import re


class GetTheme(object):
    def __init__(self, urls):
        self.session = None
        self.urls = urls
        pass

    # 获取响应
    async def resp(self, u):
        async with self.session.get(u) as response:
            return await response.text()

    # 解析
    async def parse(self, h):
        info = re.findall(r'Shopify.theme = ([\s\S]*?);', h)
        theme = json.loads(info[0])['name']
        print(theme)

    # 生成任务
    async def main(self, url, concurrent):
        async with concurrent:
            async with aiohttp.ClientSession() as self.session:
                html = await self.resp(url)
                await self.parse(html)

    def run(self):
        semaphore = asyncio.Semaphore(64)  # 限制并发数
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.main(url, semaphore)) for url in self.urls]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)


urls = ["https://kswerd.com/", "https://mlsofg.com/", "https://hallsoo.com/", "https://cveroa.com/",
        "https://qrjvxz.com/", "https://dxsro.com/", "https://kouea.com/", "https://nlrfs.com/"]
s = time.time()
get_theme = GetTheme(urls=urls)
get_theme.run()
print(time.time()-s)
