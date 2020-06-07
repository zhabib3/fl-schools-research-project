import scrapy


class School(scrapy.Item):
    district_name = scrapy.Field()
    school_name = scrapy.Field()
    website = scrapy.Field()
