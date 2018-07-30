import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
import re

### UTILITY FUNCTIONS ####
def sort_by_addr(item):
    """
    Sort function, alphanumerical order of "street name : address number"
    ITEM: to sort
    """
    return item[1] + ':' + item[0]

def csv_to_dict(filename, key_index, val_index):
    """
    KEY_INDEX is the index of the key in the new dictionary.
    VAL_INDEX is the index of the value in the new dictionary.
    """
    csv_dict = {}
    with open(filename, 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        for line in r:
            if line[key_index] not in csv_dict.keys():
                csv_dict[line[key_index]] = [line[val_index]]
            else:
                csv_dict[line[key_index]].append(line[val_index])
    return csv_dict

### PARSERS ###
def parse_addresses(addr_option='-h'):
    """
    Parses data from data/RAW_ADDR.CSV, returns sorted list of addresses
    """
    all_addr = []
    street_addr = []
    house_addr = []
    business_addr = []
    # zip_codes = []

    with open('data/raw_addr.csv', 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        for line in r:
            street_name = line[0].strip()
            zip_code = line[6][:5] # line[1] not always accurate!
            num = line[2]
            pattern = line[3]
            company = line[4].strip()
            addr_type = line[5].strip()

            if street_name == 'name':
                continue
            # zip_codes.append(zip_code)

            if addr_type == 'S':
                if len(num.split(' ')) > 1 and num.split(' ')[1] == 'to':
                    start = 0
                    end = 0
                    letter = ''
                    try:
                        start = int(num.split(' ')[0])
                        end = int(num.split(' ')[2])
                    except:
                        # this is for the 2401A/B addresses
                        start = int(num.split(' ')[0][:4])
                        end = int(num.split(' ')[2][:4])
                        letter = num.split(' ')[0][4]
                    if pattern == 'Even Only' or pattern == 'Odd Only':
                        for i in range(start, end, 2):
                            all_addr.append((str(i) + letter, street_name, zip_code))
                    else:
                        for i in range(start, end):
                            all_addr.append((str(i) + letter, street_name, zip_code))
                else:
                    street_addr.append((num, street_name, zip_code))
            if addr_type == 'H':
                house_addr.append((num, street_name, zip_code))
            if addr_type == 'F':
                business_addr.append((num, street_name, zip_code, company))

    sorted_list = []
    filename = ''
    if addr_option == '-h':
        sorted_list = house_addr
    if addr_option == '-s':
        sorted_list = all_addr
    if addr_option == '-m':
        sorted_list = street_addr
    if addr_option == '-b':
        sorted_list = business_addr

    print("# unique possible addresses: %i" % len(set(all_addr)))
    print("# unique misc addresses: %i" % len(set(street_addr)))
    print("# unique high rise addresses: %i" % len(set(house_addr)))
    print("# unique business addresses: %i" % len(set(business_addr)))
    # print("ZIP CODES: %s" % str(sorted(list(set(zip_codes)))))
    return sorted(list(sorted_list), key=sort_by_addr)

def parse_ceilings(filename):
    """
    Input CSV filename of a rent set and plot the distribution of individual rents
    """
    num_units = 0
    n = 0

    rent_units = {}
    rent_ceils = {}
    rent_occs = {}
    rent_avg = {}

    with open(filename, 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        for line in r:
            rent_ceiling = line[0]
            unit_address = line[1]
            housing_services = line[2]
            tenancy_start_date = line[3]
            unit_status = line[4]
            bed = line[5]
            occ = line[6]

            if rent_ceiling == 'rent_ceiling' or unit_address == '':
                continue
            num_units += 1

            apt_address = unit_address
            unit = ''
            if '#' in unit_address:
                end = unit_address.index('#') - 1
                apt_address = unit_address[:end]
                unit = unit_address[end + 1:]

            if rent_ceiling != 'n/a' and occ != '-1':
                ceil = float(rent_ceiling.strip('$').replace(',', ''))
                occ = int(occ)
                if occ > 0:
                    if apt_address not in rent_units.keys():
                        rent_units[apt_address] = [unit]
                        rent_ceils[apt_address] = [ceil]
                        rent_occs[apt_address] = [occ]
                    else:
                        rent_units[apt_address].append(unit)
                        rent_ceils[apt_address].append(ceil)
                        rent_occs[apt_address].append(occ)

    averages = []
    for apt_address in rent_units.keys():
        total = 0
        num_occ = 0
        for i in range(len(rent_units[apt_address])):
            # n += 1
            total += rent_ceils[apt_address][i]
            num_occ += rent_occs[apt_address][i]
        rent_avg[apt_address] = total / num_occ
        averages.append(total / num_occ)
    # plt.hist(averages,bins=40)
    # plt.show()
    return rent_avg

def main(argv):
    if len(argv) == 2 and argv[0] == '--addr':
        to_write = 'address,zip\n'
        filename = ''
        addresses = parse_addresses(argv[1])
        for item in addresses:
            to_write += item[0] + ' ' + item[1] + ',' + item[2] + '\n'

        if argv[1] == '-h': # high rises
            filename = 'data/addr.csv'
        if argv[1] == '-s': # all addresses
            filename = 'data/addr_all.csv'
        if argv[1] == '-m': # misc addresses
            filename = 'data/addr_misc.csv'
        if argv[1] == '-b': # businesses
            filename = 'data/addr_inc.csv'
        else:
            raise Exception('Unrecognized argument for ADDRESS DATA')

        f = open(filename, 'w')
        f.write(to_write)
        f.close()
        print('Wrote data to %s' % filename)

    if len(argv) > 1 and argv[0] == '--ceil':
        filename = ''
        if len(argv) == 2:
            if argv[1] == '-h':
                filename = 'data/rent.csv'
            elif argv[1] == '-s':
                filename = 'data/rent_all.csv'
            elif argv[1] == '-m':
                filename = 'data/rent_misc.csv'
            elif argv[1] == '-b':
                filename = 'data/rent_inc.csv'
        else:
            filename = 'data/rent.csv'

        parse_ceilings(filename)
    if len(argv) == 1 and argv[0] == '--rpo':
        bubbles = []
        rpo = parse_ceilings('data/rent.csv')

        missed = []
        minLat = 40.0
        maxLat = 30.0
        minLon = -120.0
        maxLon = -130.0
        with open('data/geocodes.csv', 'r') as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            for line in r:
                if line[0] in rpo.keys():
                    apt_obj = {
                        'addr': line[0],
                        'lat': line[1],
                        'lon': line[2],
                        'rpo': rpo[line[0]],
                    }
                    if float(line[1]) < minLat:
                        minLat = float(line[1])
                    if float(line[1]) > maxLat:
                        maxLat = float(line[1])
                    if float(line[2]) < minLon:
                        minLon = float(line[2])
                    if float(line[2]) > maxLon:
                        maxLon = float(line[2])
                    # bubbles.append(apt_obj)
                else:
                    missed.append(line[0])
        with open('rpo.json', 'w') as outfile:
            json.dump(bubbles, outfile)
        print(len(bubbles))
        print(len(missed))
        # print("MIN LAT: %f" % minLat)
        # print("MAX LAT: %f" % maxLat)
        # print("MIN LON: %f" % minLon)
        # print("MAX LON: %f" % maxLon)
    else:
        # arr = []
        # matched_arr = []
        # with open('data/rent.csv', 'r') as f:
        #     r = csv.reader(f, delimiter=',')
        #     for line in r:
        #         arr.append(line[1] + ': ' + line[0] + '[' + line[6] + ']')
        # with open('no_rent.txt', 'r') as g:
        #     r = csv.reader(g, delimiter=',')
        #     for line in r:
        #         for a in arr:
        #             if line[0] in a:
        #                 matched_arr.append(a)
        # for m in matched_arr:
        #     print(m)
        to_write = ''
        with open('data/geocodes.csv', 'r') as f:
            for line in f:
                split = line.split(',')
                to_write += split[0]+','+split[1]+','+split[2]+','+split[3]+','+split[4]
                for i in range(5, len(split)):
                    to_write += split[i]+'+'
                to_write = to_write[:-1]
        print(to_write)
        g = open('data/gcodes.csv', 'w')
        g.write(to_write)
        g.close()

if __name__ == "__main__":
   main(sys.argv[1:])
