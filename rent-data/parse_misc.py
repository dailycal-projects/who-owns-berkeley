import csv
import json
import matplotlib.pyplot as plt

"""
PARSE_ADDR.PY is specifically for generating addr files.
This file is for the other generating other files.
See PARSE_SHP.PY for generating shapefiles.
"""

# these are address endings that are specific to University buildings,
# which we don't have or need rent data for.
addr_ignore = ['HALL','BLDG','GYM','FACILITY','PAVILION','BUSINESS','LAB','SCIENCE',
               'ADDITION','UN','CLB','CTR','HOUSE','SERVICES','CAMPUS','EXT']
# add as necessary
translate_dict = {
    'MLK': 'MARTIN LUTHER KING',
}

# UTILS
def format_addr(addr):
    hashtag = addr.find(' #')
    if hashtag > -1:
        addr = addr[:hashtag]
    for trans in translate_dict.keys():
        if trans in addr:
            addr = addr.replace(trans, translate_dict[trans])
    return addr

def parse_ceilings():
    """
    Input CSV filename of a rent set and plot the distribution of individual rents
    """
    num_units = 0
    n = 0

    rent_units = {}
    rent_ceils = {}
    rent_occs = {}
    rent_avg = {}

    def add_ceilings(filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if row['rent_ceiling'] == 'rent_ceiling' or row['unit_address'] == '':
                    continue
                # num_units += 1
                apt_address = format_addr(row['unit_address'])

                if row['rent_ceiling'] != 'n/a' and row['occ'] != '-1':
                    ceil = float(row['rent_ceiling'].strip('$').replace(',', ''))
                    occ = int(row['occ'])
                    if occ > 0:
                        if apt_address not in rent_units:
                            rent_units[apt_address] = [row['unit_address']]
                            rent_ceils[apt_address] = [ceil]
                            rent_occs[apt_address] = [occ]
                        else:
                            rent_units[apt_address].append(row['unit_address'])
                            rent_ceils[apt_address].append(ceil)
                            rent_occs[apt_address].append(occ)

    add_ceilings('data/rent.csv')
    add_ceilings('data/rent_rest.csv')

    averages = []
    for apt_address in rent_units:
        total = 0
        num_occ = 0
        for i in range(len(rent_units[apt_address])):
            # n += 1
            total += rent_ceils[apt_address][i]
            num_occ += rent_occs[apt_address][i]
        rent_avg[apt_address] = total / num_occ
        averages.append(total / num_occ)
    # print(len(averages))
    # plt.hist(averages,bins=40)
    # plt.show()
    # with open('data/rpo.csv', 'wb') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for key, value in rent_avg.items():
            # writer.writerow([key, value])
    bubbles = []
    missed = []
    with open('data/geocodes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['address'] in rent_avg:
                apt_obj = {
                    'addr': row['address'],
                    'lat': row['lat'],
                    'lon': row['lon'],
                    'rpo': rent_avg[row['address']],
                }
                bubbles.append(apt_obj)
            else:
                missed.append(row['address'])
    with open('rpo.json', 'w') as outfile:
        json.dump(bubbles, outfile)
    print(len(bubbles))
    print(len(missed))
    return rent_avg

# Get all addresses that are possible in ADDR_ALL but not in
# existing addresses in ADDR (the rest)
def get_addr_rest():
    all_addr = []
    with open('data/addr_all.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_addr.append(row['address'])

    addr = []
    with open('data/addr.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            addr.append(row['address'])

    print(len(set(all_addr)))
    print(len(set(addr)))
    nonh_addr = set.union(set(all_addr), set(addr)) - set.intersection(set(all_addr), set(addr))
    print(len(nonh_addr))
    w = 'address\n'
    for a in nonh_addr:
        w += a + '\n'
    f = open('data/addr_rest.csv', 'w')
    f.write(w)
    f.close()

def parse_owners():
    named_addresses = []
    owners = []
    with open('data/owners.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            named_addresses.append(row['address'])
            owners.append(row['owner'])

    missed = []
    for a in addresses:
        if a not in named_addresses:
            st = a.split(' ')[-1]
            if st == 'Hall' or st == 'Bldg' or st == 'Gym' or st == 'Facility' or st == 'Pavilion' or st == 'Business' or st == 'Lab' or st == 'Science' or st == 'Addition' or st == 'Un' or st == 'Clb' or st == 'Ctr' or st == 'House' or st == 'Services' or st == 'Campus' or st == 'Ext':
                continue
            missed.append(a)
            print(a)
    print(missed)

    freq_dict = {}
    for o in owners:
        if o not in freq_dict.keys():
            freq_dict[o] = 1
        else:
            freq_dict[o] += 1

    li = sorted(freq_dict.items(), key=lambda x: -x[1])
    f = open('owners_by_properties.csv', 'w')
    g = open('lakireddies.csv', 'w')
    to_write = ''
    lakireddies = ''
    for l in li:
        to_write += l[0] + ',' + str(l[1]) + '\n'
        if 'LAKIREDDY' in l[0]:
            lakireddies += l[0] + ',' + str(l[1]) + '\n'
    f.write(to_write)
    f.close()
    g.write(lakireddies)
    g.close()

# Take input RENT file and find all unique addresses,
# not including units
def get_unique_addr():
    unique_addr = 'address\n'

    numrows = 0
    with open('data/rent.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            numrows += 1
            unit = row['unit_address']
            unit = format_addr(unit)
            if unit not in unique_addr:
                unique_addr += unit.upper() + '\n'
    with open('data/rent_rest.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            numrows += 1
            unit = row['unit_address']
            unit = format_addr(unit)
            if unit not in unique_addr:
                unique_addr += unit.upper() + '\n'
    print(numrows)
    f = open('data/address.csv', 'w')
    f.write(unique_addr)
    f.close()

    addresses = []
    with open('data/addr_all.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            addresses.append(row['address'].upper())

    print(len(addresses))

    # missed = []
    # for addr in addresses:
    #     if addr not in unique_addr:
    #         missed.append(addr)
    #         # print(a)
    #
    # print(len(missed))

def main():

    # with open('data/rent.csv') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:


main()
