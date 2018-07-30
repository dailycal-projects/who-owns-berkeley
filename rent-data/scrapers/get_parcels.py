import scrapy
import csv
from num2words import num2words
import re

base_url = 'https://www.cityofberkeley.info'

addresses = []
with open('../data/address.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        addresses.append(row['address'])
"""
Here are some test addresses to make sure the lookups aren't failing.
For example, inconsistences in the city record between choice of
"MLK JR WAY" or "MARTIN LUTHER KING JR WAY", and "5TH" or "FIFTH".
"""
# addresses = ['5230 DWIGHT WAY', '1734 HIGHLAND PL', '1708 MARTIN LUTHER KING JR WAY',
             # '1711 MARTIN LUTHER KING JR WAY', '2430 5th St', '1608 62nd St']
# missed_addresses = []

class ParcelSpider(scrapy.Spider):
    name = 'parcelspider'
    start_urls = ['https://www.cityofberkeley.info/ppop']
    download_delay = 0.01

    def reformat(self, addr):
        r = addr
        r = r.replace('MARTIN LUTHER KING JR', 'M L KING JR')
        r = r.replace(' 1/2', '')
        split = r.split(' ')
        match = re.search('\d+', split[1])
        if len(split) > 2 and match is not None:
            ordinal = int(match.group(0))
            split[1] = num2words(ordinal, to='ordinal').upper()
        r = " ".join(split)
        return r

    def parse(self, response):
        for addr in addresses:
            reformatted_address = self.reformat(addr)
            yield scrapy.FormRequest(
                'https://www.cityofberkeley.info/ppop/home/FindByAddress',
                meta = {
                    'address': addr,
                    'reformatted_address': reformatted_address
                },
                formdata = {
                    'StreetNumber': reformatted_address.split(' ')[0],
                    'StreetName': reformatted_address.split(' ')[1:-1],
                    'StreetSuffix': reformatted_address.split(' ')[-1],
                },
                callback = self.parse_addr,
            )

    def parse_addr(self, response):
        units = list(set(response.css('td a ::attr(href)').extract()))
        if 'NoResults' in response.url:
            yield {
                'address': response.meta['address'],
                'owner': 'FAILED_LOOKUP',
            }
        else:
            for unit in units:
                yield scrapy.Request(
                    base_url + units[0],
                    meta = {
                        'address': response.meta['address']
                    },
                    callback = self.parse_owner,
                )

    def parse_owner(self, response):
        row = response.css("tr")[5]
        owner = row.css('td ::text')[1].extract()
        yield {
            'address': response.meta['address'].upper(),
            'owner': owner.replace('&amp;','&').strip(),
        }
