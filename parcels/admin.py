from django.contrib import admin
from parcels.models import Parcel

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    pass
