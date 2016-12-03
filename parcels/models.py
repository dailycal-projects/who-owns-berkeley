from django.contrib.gis.db import models

class ScrapedParcel(models.Model):
    url = models.CharField(
        max_length=256
    )
    scraped_datetime = models.DateTimeField(
        auto_now=True
    )
    address_type = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    full_address = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    owner = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    county_use_description = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    lot_size = models.FloatField(
        null=True,
        blank=True,
        default=None
    )
    building_size = models.FloatField(
        null=True,
        blank=True,
        default=None
    )

    parcel = models.ForeignKey(
        'Parcel',
        related_name='scraped_records'
    )
    APN = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.parcel__parcelid


class Parcel(models.Model):
    city = models.CharField(max_length=254)
    condo = models.CharField(max_length=254)
    direction = models.CharField(max_length=254)
    parcelid = models.CharField(
        max_length=254,
        unique=True
    )
    state = models.CharField(max_length=254)
    streetname = models.CharField(max_length=254)
    streetsufx = models.CharField(max_length=254)
    unit = models.CharField(max_length=254)
    usecd = models.CharField(max_length=254)
    usedscrp = models.CharField(max_length=254)
    zip = models.CharField(max_length=254)

    bldgarea = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    lotsqft = models.FloatField()
    shape_star = models.FloatField()
    shape_stle = models.FloatField()
    streetnum = models.FloatField()
    x_min = models.FloatField()
    x_max = models.FloatField()
    y_min = models.FloatField()
    y_max = models.FloatField()

    url = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    
    geom = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    def __str__(self):
        return self.parcelid