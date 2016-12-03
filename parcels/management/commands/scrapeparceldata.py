import requests
from django.utils import timezone
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from parcels.models import Parcel, ScrapedParcel


class Command(BaseCommand):
    """
    Scrape parcel data from city website. 
    """
    help = "Scrape parcel data from city website. "

    def handle(self, *args, **options):
        endpoint = 'http://www.cityofberkeley.info'
        for parcel in Parcel.objects.exclude(url=None).filter(
                scraped_records=None):

            print(parcel.parcelid)

            # Get the HTML
            url = endpoint + parcel.url 
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            # Create scraped data dict with url and parcel object
            data = {
                'url': url,
                'parcel': parcel,
            }

            columns = [
                'address_type',
                'APN',
                'full_address',
                'lot_size',
                'building_size',
                'owner',
                'county_use_description'
            ]

            table = soup.find('table')

            if table:
                # Populate scraped data dict
                for i, row in enumerate(table.find_all('tr')):
                    if i < 7:
                        val = row.find_all('td')[1].text.strip().upper()
                        if val == '':
                            val = None
                        data[columns[i]] = val

                # Create the record
                scrapedparcel, c = ScrapedParcel.objects.get_or_create(**data)
            else:
                print('Error')
