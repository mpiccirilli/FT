from scrapy.spider import Spider
from scrapy.selector import Selector

from FT.items import FTItem

Search = raw_input("What would you like to search FT.com? ")

beg_url = "http://search.ft.com/search?q=%r" % Search
end_url = '&t=all&rpp=100&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&f=category%5B"article"%5D%5B"Articles"%5D&ftsearchType=on&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true'

class FTSpider(Spider):
	name = "FT"
	allowed_domains = ["FT.com"]
	start_urls = [beg_url+end_url]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//ol/li')
		items = []
		for site in sites:
			item = FTItem()
			item['title'] = site.xpath('h3/a/text()').extract()
			item['link'] = site.xpath('h3/a/@href').extract()
			item['date'] = site.xpath('div/div/p/text()').extract()
			item['company'] = Search
			items.append(item)
		return items
