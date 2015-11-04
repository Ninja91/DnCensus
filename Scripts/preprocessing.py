#!/usr/bin/python

__author__ = 'Nitin'


import marisa_trie as mt
from csv import DictReader
# import cPickle as Pickle


def index_ip6address_4_aaaa():
    ip6_list = []
    ip6_trie_list = []

    with open('../records/aaaa.csv', 'r') as f:
        reader = DictReader(f)
        print reader.fieldnames

        for row in reader:
            ip6_list.append(row[reader.fieldnames[2]])
            if len(ip6_list) > 14000000:
                ip6_trie_list.append(mt.Trie(ip6_list))
                ip6_list = []
                print "Success"
                break
                

        # data = open('index1.pkl', 'wb')
        # Pickle.dump(ip6_address_list, data)

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
index_ip6address_4_aaaa()
