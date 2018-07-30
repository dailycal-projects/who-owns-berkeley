# Takes input data and converts it to a .shp (Shapefile)
# for use in QGIS.

import shapefile
import csv

w = shapefile.Writer(shapeType=shapefile.POINT)

owners = {}
with open('data/owners.csv') as ownerfile:
    oreader = csv.DictReader(ownerfile)
    for row in oreader:
        owners[row['address']] = row['owner']

rpo = {}
with open('data/rpo.csv') as rpofile:
    rporeader = csv.DictReader(rpofile)
    for row in rporeader:
        rpo[row['address']] = row['rpo']

# errors = []

with open('data/geocodes.csv') as geofile:
    georeader = csv.DictReader(geofile)
    header = georeader.fieldnames
    [w.field(field) for field in header]
    w.field('OWNER')
    w.field('AVGRENT','N',decimal=10)
    for row in georeader:
        w.point(float(row['lon']), float(row['lat']))
        o = "UNKNOWN OWNER"
        if row['address'] in owners:
            o = owners[row['address']]
        r = 0
        if row['address'] in rpo:
            r = rpo[row['address']]
            rec = [row[field] for field in header]
            rec.append(o)
            rec.append(r)
            w.record(*rec)

# print(len(errors))
w.save('shapefiles/test/geocodes')
