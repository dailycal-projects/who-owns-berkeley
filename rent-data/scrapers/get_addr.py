import scrapy
"""
Note: you can only do about 80 page lookups before the IP is blocked.
Once you've exhausted the lookups by this crawler, hop onto the next VPN.
"""


# These are the zip codes in Berkeley
zip_codes = [94702, 94703, 94704, 94705, 94707, 94708, 94709, 94710, 94720]
url = 'http://w10.melissadata.com/lookups/'

class AddressSpider(scrapy.Spider):
    name = 'addressspider'
    start_urls = ["http://w10.melissadata.com/lookups/zipstreet.asp?InData=94720"]
    download_delay = 1.5

    def parse(self, response):
        streets = response.css("tr[onmouseover=\"this.bgColor='#ffffaa';\"] a ::attr(href)").extract()
        streets_limited = streets[80:] # change this range as needed
        for name in streets_limited:
            yield scrapy.Request(
                url + name,
                callback = self.parse_streets,
            )

    def parse_streets(self, response):
        addresses = response.css("tr[onmouseover=\"this.bgColor='#ffffaa';\"]")
        for row in addresses:
            row_data = row.css("td")
            yield {
                'num/range': row_data[0].css("::text").extract_first(),
                'pattern': row_data[0].css("div ::text").extract_first(),
                'name': row_data[2].css("::text").extract_first(),
                'zip': 94720,
                'zip+4': row_data[3].css("::text").extract_first(),
                'type': row_data[4].css("::text").extract_first(),
                'company': row_data[5].css("::text").extract_first(),
            }
