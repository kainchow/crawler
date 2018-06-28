# -*- coding: utf-8 -*-
import json
from scrapy import Spider, Request
from ..items import TujiaItem
from ..settings import FORM_DATA, UNIT_ID


class CommentsSpider(Spider):
	name = 'comments'
	allowed_domains = ['www.tujia.com']
	start_urls = 'https://www.tujia.com/bingo/pc/comment/searchUnitComments'
 
 
	def start_requests(self):
		for unitid in UNIT_ID:
			FORM_DATA['unitId'] = unitid
			formdata = FORM_DATA
			yield self.make_requests_from_url(formdata)
	
	def make_requests_from_url(self, formdata):
		return Request(self.start_urls, method='POST', body=json.dumps(formdata), callback=self.parse)
	
	def parse(self, response):
		data = json.loads(response.text).get('data')
		comments = data.get('comments')
		if comments:
			for comment in comments:
				item = TujiaItem()
				for field in item.fields:
					item[field] = comment.get(field)
				yield item