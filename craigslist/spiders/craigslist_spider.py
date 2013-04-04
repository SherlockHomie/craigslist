from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem


def _selector_regex(selector, regex):
    try:
        return selector.re(regex)[0]
    except IndexError:
        return None


class CraigslistSpider(BaseSpider):
    name = 'craigslist'
    allowed_domains = [
        'sfbay.craigslist.org',
    ]
    start_urls = [
        'http://sfbay.craigslist.org/sfc/apa/',
        'http://sfbay.craigslist.org/sfc/roo/',
    ]
    def parse(self, response):
        '''Parses a craigslist response.

        @url http://sfbay.craigslist.org/apa/
        @returns items 50
        @scrapes title link price neighborhood
        '''
        hxs = HtmlXPathSelector(response)
        items = []
        rows = hxs.select("//p[@class='row']")
        for row in rows:
            item = CraigslistItem()
            link = row.select("span[@class='pl']")
            item['title'] = link.select('a/text()').extract()
            item['link'] = link.select('a/@href').extract()
            itempnr = row.select("span[@class='itempnr']")
            price_br_sqft = itempnr.select('text()')
            item['price_br_sqft'] = price_br_sqft.extract()[0]
            item['price'] = int(_selector_regex(price_br_sqft, r' \$(\d+(?:,\d+)?)'))
            item['neighborhood'] = itempnr.select('font[@size="-1"]/text()').extract()
            items.append(item)
        return items
