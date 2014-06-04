from scrapy.item import Item, Field

class FTItem(Item):
    title = Field()
    link = Field()
    date = Field()
    company = Field()
