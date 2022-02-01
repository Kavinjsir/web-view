import scrapy
import re
import json

class GnewsSpider(scrapy.Spider):
    name = "gnews"

    keyword1 = "booster"
    keyword2 = "omicron"

    start_urls = [
        f'https://news.google.com/search?q={keyword1}+{keyword2}&hl=en-US&gl=US&ceid=US%3Aen'
    ]

    def parse(self, response):
        titles = re.findall(r'<h3 class="[^"]+?"><a[^>]+?>(.+?)</a>', response.text)

        filename = f'{self.keyword1}_{self.keyword2}.json'
        with open(filename, 'w') as f:
            json.dump(titles, f)
        self.log(f'Saved file {filename}')
