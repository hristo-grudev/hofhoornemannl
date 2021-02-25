import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import HofhoornemannlItem
from itemloaders.processors import TakeFirst


class HofhoornemannlSpider(scrapy.Spider):
	name = 'hofhoornemannl'
	start_urls = ['https://www.hofhoorneman.nl/nieuws']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-md-4 mb-4"]/a[1]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2//text()').get()
		description = response.xpath('//div[@class="col-md-8 order-2 order-md-1"]//text()[normalize-space() and not (ancestor::h2)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-9 news-date gray-text"]/text()').getall()
		if date:
			date = [p.strip() for p in date]
			date = ' '.join(date).strip()
			date = re.findall(r'\d+-\d+-\d+', date)

		item = ItemLoader(item=HofhoornemannlItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
