"""
抓取猫眼电影top一百
"""
import requests
from requests.exceptions import RequestException
from lxml import etree
from pprint import pprint


class Film:
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset=0"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    def get_url(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.content.decode()
            return None
        except RequestException:
            return None

    def parse(self, html):
        element = etree.HTML(html)
        next_page_url = element.xpath("//a[text()='下一页']/@href")
        dd_list = element.xpath("//dl[@class='board-wrapper']/dd")
        for dd in dd_list:
            item = dict()
            item["index"] = dd.xpath(".//i[contains(@class,'board-index')]/text()")[0]
            item["title"] = dd.xpath(".//p[@class='name']/a/@title")[0]
            item["star"] = dd.xpath(".//p[@class='star']/text()")[0].strip()
            item["release_time"] = dd.xpath(".//p[@class='releasetime']/text()")[0]
            pprint(item)
        if len(next_page_url) > 0:
            next_page_url = "https://maoyan.com/board/4" + element.xpath("//a[text()='下一页']/@href")[0]
            html2 = self.get_url(next_page_url)
            return self.parse(html2)

    def main(self):
        html = self.get_url(self.url)
        items = self.parse(html)


if __name__ == '__main__':
    film = Film()
    film.main()
