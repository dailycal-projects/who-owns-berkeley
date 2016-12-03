import csv
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from parcels.models import Parcel, ScrapedParcel

class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        """with open('out.csv','w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['APN','url'])

            for parcel in Parcel.objects.all():
                writer.writerow([parcel.parcelid, parcel.url])"""

        with open('out.csv','r') as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                parcel = Parcel.objects.get(parcelid = row['APN'])
                parcel.url = row['url']
                parcel.save()