import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from parcels.models import Parcel


class Command(BaseCommand):
    """
    Scrape parcel urls from city website using parcel APN.
    """
    help = "Scrape parcel urls from city website."

    def handle(self, *args, **options):
        endpoint = 'http://www.cityofberkeley.info/ppop/home/FindByAPN'
        for parcel in Parcel.objects.all():
            print(parcel.parcelid)
            data = {
                'PropertyApn': parcel.parcelid
            }
            r = requests.post(endpoint, data)
            soup = BeautifulSoup(r.text, 'html.parser')
            url = soup.find('table').find('a')['href']
            print(url)

            parcel.url = url
            parcel.save()
