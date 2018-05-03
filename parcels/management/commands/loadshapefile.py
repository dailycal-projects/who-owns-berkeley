import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from parcels.models import Parcel


class Command(BaseCommand):
    help = "Load parcels from shapefile."

    def handle(self, *args, **options):
        Parcel.objects.all().delete()
        path = os.path.join(
            settings.BASE_DIR,
            'data',
            'parcels.shp')

        parcel_mapping = {
                'city': 'city',
                'condo': 'condo',
                'direction': 'direction',
                'parcelid': 'parcelid',
                'state': 'state',
                'streetname': 'streetname',
                'streetsufx': 'streetsufx',
                'unit': 'unit',
                'usecd': 'usecd',
                'usedscrp': 'usedscrp',
                'zip': 'zip',
                'bldgarea': 'bldgarea',
                'latitude': 'latitude',
                'longitude': 'longitude',
                'lotsqft': 'lotsqft',
                'shape_star': 'shape_star',
                'shape_stle': 'shape_stle',
                'streetnum': 'streetnum',
                'x_min': 'x_min',
                'x_max': 'x_max',
                'y_min': 'y_min',
                'y_max': 'y_max',
                'geom' : 'MULTIPOLYGON'
        }

        lm = LayerMapping(
            Parcel,
            path,
            parcel_mapping,
            source_srs=SpatialReference(4326))
        lm.save(verbose=True)
