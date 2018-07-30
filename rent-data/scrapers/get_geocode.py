import requests
import csv
import json

API_KEY_1 = '' # use your Google Maps API Key
API_KEY_2 = '' # if you have multiple Google accounts,
API_KEY_3 = '' # rotate through all of them
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='

addresses = []

with open('../data/address.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['address'] not in addresses:
            addresses.append(row['address'])

to_write = 'pid,lat,lon,address,formatted_address\n'
for i in range(len(addresses)):
    apt_address = addresses[i]
    get_url = url + apt_address.replace(' ', '+') + ',+BERKELEY,+CA&key='
    # if i%2 == 0:
    #     get_url += API_KEY_1
    # else:
    #     get_url += API_KEY_2
    get_url += API_KEY_1
    response = requests.get(get_url)
    data = json.loads(response.content)
    status = data['status']

    if status == 'OK':
        loc = data['results'][0]['geometry']['location']
        to_write += data['results'][0]['place_id'] + ','
        to_write += str(loc['lat']) + ',' + str(loc['lng']) + ','
        to_write += apt_address + ','
        to_write += data['results'][0]['formatted_address'].replace(',','+') + '\n'
    else:
        to_write += 'n/a,n/a,n/a,' + apt_address + ',n/a\n'
    print(i, status, apt_address)

f = open('../data/geocodes.csv', 'w')
f.write(to_write)
f.close()
