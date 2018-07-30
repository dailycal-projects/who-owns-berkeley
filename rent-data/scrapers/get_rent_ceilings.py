import scrapy
import csv

addresses = []
with open('../data/addr_rest.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['address'] not in addresses:
            addresses.append(row['address'])

class RentCeilingSpider(scrapy.Spider):
    name = 'rentceilingspider'
    start_urls = ['https://www.cityofberkeley.info/RentBoardUnitSearch.aspx']
    download_delay = 0.01

    def parse(self, response):
        for address in addresses:
            yield scrapy.FormRequest(
                'https://www.cityofberkeley.info/RentBoardUnitSearch.aspx',
                formdata = {
                    # THIS IS THE ADDRESS INPUT
                    'ctl00$Col2ContentPlaceholder$txtSearchInput': address,
                    # THE REST ARE CONSTANT ENVIRONMENT VARIABLES
                    'ctl00$Col2ContentPlaceholder$ScriptManager1': 'ctl00$Col2ContentPlaceholder$UpdatePanel1|ctl00$Col2ContentPlaceholder$imgbtnSearch',
                    'ctl00$Col2ContentPlaceholder$imgbtnSearch.x': '0',
                    'ctl00$Col2ContentPlaceholder$imgbtnSearch.y': '0',
                    'EktronClientManager': response.css('input#EktronClientManager::attr(value)').extract_first(),
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                    '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    # '__ASYNCPOST': 'false',
                },
                callback = self.parse_results,
        )

    def parse_results(self, response):
        print(response.css("#ctl00_Col2ContentPlaceholder_txtSearchInput::attr(value)").extract_first())
        for row in response.css("#ctl00_Col2ContentPlaceholder_ucRentBoardUnitList_gvRentBoardUnitList tr:not(.gridHeader)"):
            unit_address = row.css(".rentControlledUnitOptionsOuterContainer span ::text").extract_first()
            numbers = row.css(".gridItem span ::text").extract()
            text = row.css(".gridItem p").extract()
            num_bed = -1
            if text[2].find('# Bed:') != -1:
                start = text[2].find('# Bed:') + 7
                end = text[2].find('<br>')
                num_bed = int(text[2][start:end])
            num_occ = -1
            if text[2].find('# Occ:') != -1:
                start = text[2].find('# Occ:') + 7
                end = text[2].find('<br>', start)
                num_occ = int(text[2][start:end])
            yield {
                'unit_address': unit_address,
                'tenancy_start_date': numbers[0],
                'rent_ceiling': numbers[1],
                'unit_status': text[0],
                'housing_services': text[1],
                'bed': num_bed,
                'occ': num_occ,
            }
