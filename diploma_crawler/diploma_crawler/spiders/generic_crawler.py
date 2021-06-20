import csv
import json
from datetime import datetime
from pathlib import Path

import spacy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.httpobj import urlparse
from bs4 import BeautifulSoup
import html2text

from diploma_crawler.helper import get_tag_rules

MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / "model"


class GenericCrawlerSpider(CrawlSpider):
    name = "generic_crawler"
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, url=None, classes=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not url:
            return
        self.allowed_domains = [urlparse(url).netloc]
        self.start_urls = [f'{urlparse(url).scheme}://{urlparse(url).netloc}/']
        self.nlp = spacy.load(MODEL_PATH)
        self.classes = json.loads(classes)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in get_tag_rules():
            for div in soup.select(tag):
                div.extract()

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True
        text = " ".join(converter.handle(soup.find("body").get_text()).split('\n'))
        print(text)

        name = self.allowed_domains[0] + '-' + datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        with open(Path(__file__).resolve().parent.parent.parent.parent / "files" / f'{name}.txt', 'w', encoding='utf-8') as file:
            file.write(text)

        doc = self.nlp(text)
        with open(Path(__file__).resolve().parent.parent.parent.parent / "files" / f'{name}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["url", "file", "span", "label", "start", "end"])
            for ent in doc.ents:
                if ent.label_ in self.classes:
                    writer.writerow([response.request.url, name, ent.text, ent.label_, ent.start_char, ent.end_char])
