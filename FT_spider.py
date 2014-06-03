from scrapy.spider import Spider
from scrapy.selector import Selector

from FT.items import FTItem

class FTSpider(Spider):
	name = "FT"
	allowed_domains = ["FT.com"]
	start_urls = ["http://search.ft.com/search?q=&t=all&rpp=100&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&f=category[%22article%22][%22Articles%22]&f=organisations[%22IMAX+Corp%22][%22IMAX+Corp%22]&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true", "http://search.ft.com/search?q=General+Motors+Co&t=all&rpp=100&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&f=category[%22article%22][%22Articles%22]&ftsearchType=type_news&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true", "http://search.ft.com/search?q=Sprint+Nextel+Corp&t=all&rpp=100&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&ftsearchType=type_news&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true"]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//ol/li')
		items = []
		for site in sites:
			item = FTItem()
			item['title'] = site.xpath('h3/a/text()').extract()
			item['link'] = site.xpath('h3/a/@href').extract()
			item['date'] = site.xpath('div/div/p/text()').extract()
			items.append(item)
		return items
