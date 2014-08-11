import pandas as pd
from scrapy.spider import Spider
from scrapy.selector import Selector

from FT.items import FTItem


#list the files available
#print "Here is alist of the companies available:"
#print glob.glob("/Users/michaelpiccirilli/Documents/Learning_Pything/Scrapy/FT/*.json")

#get_name = raw_input("type in the full filename name you would like to import: ")
#file_name = "%r" % get_name

#print file_name

data = pd.read_json("amazon.json")

links = []

for row in data:
    links.append(data['link'])
    

for i in links:
    
    class FTSpider(Spider):
            name = "FT"
            allowed_domains = ["FT.com"]
            start_urls = [i]

            def parse(self, response):
                    sel = Selector(response)
                    sites = sel.xpath('//*[@id="storyContent"]')
                    items = []
                    for site in sites:
                            item = FTItem()
                            item['body'] = site.xpath('p/text()').extract()
                            items.append(item)
                    return items
