"""
爬虫模块
"""
import re
import json
import asyncio
import aiohttp
import aiomysql
import requests
from lxml import etree
from fake_useragent import UserAgent


ua = UserAgent()
head = {
    'User-Agent': ua.random
}


class Reptile(object):
    def __init__(self, domain):
        self.domain = domain
        self.fir = domain+'/collections/all'
        self.session = None
        self.head = head
        self.rules = None
        pass

    def main(self):
        """
        同步代码，生成所有page
        :return:
        """
        with requests.get(
                url=self.fir,
                headers=self.head
        )as response:
            info = re.findall(r'Shopify.theme = ([\s\S]*?);', response.text)
            theme = json.loads(info[0])['name']
            print(theme)
            data = requests.get(f'http://127.0.0.1:5000/api/rules/{theme}')
            """
            {
              "data": {
                "describe": "Debut主题",
                "rules": {
                  "goods_link": "//div[@id='Collection']/ul/li/div/a/@href",
                  "goods_name": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[1]/h1/text()",
                  "goods_norms": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[2]/p/span/strong/text()",
                  "goods_price": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[1]/div/dl/div[1]/div[1]/dd/span/text()",
                  "goods_value": "/html/body/div[3]/main/div[1]/div/div/div[2]/div[2]/p/span/text()",
                  "img_links": "//div[contains(@class,'thumbnails-wrapper')]/ul/li/a/@href",
                  "page": "/html/body/div[3]/main/div/div/div/ul[2]/li[2]/text()"
                },
                "theme": "Debut"
              },
              "msg": "success"
            }
            """
            if data.status_code == 200:
                data = data.json()
                self.rules = data['data']['rules']
            else:
                return
            html = etree.HTML(response.text)
            page_info = html.xpath(self.rules['page'])  # 页码的xpath
            all_url = []
            for pages in page_info:
                page = re.findall(f'\d+', pages)[1]
                for i in range(1, int(page)+1):
                    url = self.fir + f'?page={i}'
                    # print(url)
                    with requests.get(url) as response:
                        html = etree.HTML(response.text)
                        u_list = html.xpath(self.rules['goods_link'])  # 页面商品链接
                        for u in u_list:
                            all_url.append(self.domain + u)
            return all_url

    async def get(self, loop, url):
        pool = await aiomysql.create_pool(host='47.97.166.98', port=3306,
                                          user='root', password='100798',
                                          db='yzz', loop=loop, autocommit=True, charset='utf8')
        async with aiohttp.ClientSession() as self.session:
            content = await self.par(url)  # 跳到par()
            html = etree.HTML(content)
            goods_name = html.xpath(self.rules['goods_name'])[0].strip().replace('/', '').replace('*', '_')  # 商品名
            goods_price = html.xpath(self.rules['goods_price'])[0].strip()  # 商品价格

            # 提取规格，几乎完全tmd不用改，2020年3月18日15:41:23
            info = re.findall(r'var meta = ([\s\S]*?);', content)[0]
            sku_ = re.findall(r'"public_title":"(.*?)"', info)
            s_id_ = re.findall(r'"sku":"(.*?)"', info)
            s_price_ = re.findall(r'"price":(\d+)', info)
            specs_ = dict()
            all_specs = []
            for sku, s_id, s_price in zip(sku_, s_id_, s_price_):
                # print(sku, s_id, s_price)
                specs = dict()
                specs["sku"] = sku.replace('\\', '')
                specs["s_id"] = s_id
                specs["s_price"] = int(s_price)/100
                all_specs.append(specs)
            specs_["specs"] = all_specs

            # 商品属性
            goods_norms = html.xpath(self.rules['goods_norms'])
            goods_value = html.xpath(self.rules['goods_value'])
            norms = dict()  # 这个是json， ok
            for n, v in zip(goods_norms, goods_value):
                norms[n.strip()] = v.strip()
            # 图片链接
            links = dict()
            link_list = html.xpath(self.rules['img_links'])
            links["links"] = link_list

            data = dict()
            data["tittle"] = goods_name
            data["price"] = goods_price
            data["domain"] = self.domain
            data["link"] = url
            data["sku"] = json.dumps(specs_)
            data["specs"] = json.dumps(norms)
            data["img_link"] = json.dumps(links)
            # print(data)

            # 整一个异步连接池，使用异步插入
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    insert = "INSERT IGNORE INTO shopify(tittle,price,domain,link,sku,specs,img_link) VALUES " \
                             "(\'%s\','%s','%s','%s',\'%s\',\'%s\',\'%s\')" % \
                             (aiomysql.escape_string(data["tittle"]), data["price"], data["domain"], data['link'],
                              aiomysql.escape_string(data["sku"]), aiomysql.escape_string(data["specs"]),
                              aiomysql.escape_string(data["img_link"]))
                    # print(insert)
                    await cur.execute(insert)

    async def par(self, url):
        async with self.session.get(url, headers=self.head) as response:
            return await response.text()
        pass

    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)

        tasks = [asyncio.ensure_future(self.get(loop, u)) for u in self.main()]  # 把所有页面的url加入任务列表，main()
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)
