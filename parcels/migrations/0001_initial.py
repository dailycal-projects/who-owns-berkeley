# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 06:14
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=254)),
                ('condo', models.CharField(max_length=254)),
                ('direction', models.CharField(max_length=254)),
                ('parcelid', models.CharField(max_length=254, unique=True)),
                ('state', models.CharField(max_length=254)),
                ('streetname', models.CharField(max_length=254)),
                ('streetsufx', models.CharField(max_length=254)),
                ('unit', models.CharField(max_length=254)),
                ('usecd', models.CharField(max_length=254)),
                ('usedscrp', models.CharField(max_length=254)),
                ('zip', models.CharField(max_length=254)),
                ('bldgarea', models.FloatField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('lotsqft', models.FloatField()),
                ('shape_star', models.FloatField()),
                ('shape_stle', models.FloatField()),
                ('streetnum', models.FloatField()),
                ('x_min', models.FloatField()),
                ('x_max', models.FloatField()),
                ('y_min', models.FloatField()),
                ('y_max', models.FloatField()),
                ('url', models.CharField(blank=True, max_length=256, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapedParcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('scraped_datetime', models.DateTimeField(auto_now=True)),
                ('address_type', models.CharField(blank=True, max_length=256, null=True)),
                ('full_address', models.CharField(blank=True, max_length=256, null=True)),
                ('owner', models.CharField(blank=True, max_length=256, null=True)),
                ('county_use_description', models.CharField(blank=True, max_length=256, null=True)),
                ('lot_size', models.FloatField(blank=True, default=None, null=True)),
                ('building_size', models.FloatField(blank=True, default=None, null=True)),
                ('APN', models.CharField(blank=True, max_length=256, null=True)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scraped_records', to='parcels.Parcel')),
            ],
        ),
    ]
