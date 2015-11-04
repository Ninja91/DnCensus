#!/usr/bin/python

__author__ = 'Nitin'


import marisa_trie as mt
from csv import DictReader
import os.path
import cPickle as Pickle


def index_ip6address_4_aaaa():
    if os.path.isfile('index.marisa'):
        print 'Loaded'
        trie = mt.Trie().load('index.marisa')
        print trie['::ffff:74.117.221.143']
        return [trie]

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
        ip6_trie_list.append(mt.Trie(ip6_list))
        ip6_trie_list[0].save('index.marisa')
        Pickle.dump(ip6_trie_list[0], 'index.pkl')

        print "Success"
        return ip6_trie_list


def build_map(ip6_trie_list, filename='../records/aaaa.csv'):
    with open(filename, 'r') as f:
        reader = DictReader(f)
        current = None
        current_host = None
        count = 0
        i = 0

        keys = []
        values = []
        if len(ip6_trie_list) == 1:
            ip6_dict = ip6_trie_list[0]

        for row in reader:
            i += 1
            if i >= 5:
                print keys, values
                break
            prev = current
            current = row[reader.fieldnames[2]]
            print prev, current
            prev_host = current_host
            current_host = row[reader.fieldnames[0]]
            print prev_host, current_host
            if prev_host != current_host:
                keys.append(prev_host)
                values.append((ip6_dict.key_id(prev), count))
                count = 1
            else:
                if prev != current:
                    keys.append(prev_host)
                    values.append((ip6_dict.key_id(prev), count))
                    count = 1
                else:
                    count += 1


dictionary = index_ip6address_4_aaaa()
# print dictionary['::ffff:74.117.221.143']
# build_map(dictionary)
