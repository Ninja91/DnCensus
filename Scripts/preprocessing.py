#!/usr/bin/python

__author__ = 'Nitin'
from csv import DictReader
import cPickle as Pickle

BP = dict()
with open('aaaa.csv', 'rb') as f:
    reader = DictReader(f)
    print reader.fieldnames

    for row in reader:

    # for row in reader:
    #     if BP.has_key(row['name']):
    #         if row['ip4address'] in BP[row['name']]:
    #             continue
    #         else:
    #             BP[row['name']].append(row['ip4address'])
    #     else:
    #         BP[row['name']] = [row['ip4address']]
    #
    # f = open('map.pkl', 'wb')
    # Pickle.dump(BP, f)
