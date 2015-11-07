#!/usr/bin/python

__author__ = 'Nitin'

import marisa_trie as mt
from csv import DictReader
import os.path
import marshal as Pickle
from backports import lzma as lz

IP6_INDEX_FILE = '_ip6_index.marisa'
NAME_INDEX_FILE = '_name_index.marisa'


def index_ip6address_4_aaaa(filename='../records/aaaa.csv'):
    ip6_index_fn = filename.replace('.csv', IP6_INDEX_FILE)
    name_index_fn = filename.replace('.csv', NAME_INDEX_FILE)

    if os.path.isfile(ip6_index_fn) and os.path.isfile(name_index_fn):
        return [mt.Trie().load(NAME_INDEX_FILE)], [mt.Trie().load(IP6_INDEX_FILE)]
        print 'Loaded'

    ip6_list = []
    name_list = []
    name_trie_list = []
    ip6_trie_list = []

    with open(filename, 'rb') as f:
        print f
        reader = DictReader(f)
        print reader.fieldnames
        i = 0

        for row in reader:
            i += 1
            if i % 10000000 == 0:
                print i
                
            ip6_list.append(row[reader.fieldnames[2]])
            name_list.append(row[reader.fieldnames[0]])
            # if len(ip6_list) > 14000000:
            #     ip6_trie_list.append(mt.Trie(ip6_list))
            #     ip6_list = []
            #     print "Success"
            #     break
        ip6_trie_list.append(mt.Trie(ip6_list))
        name_trie_list.append(mt.Trie(name_list))
        ip6_trie_list[0].save(ip6_index_fn)
        name_trie_list[0].save(name_index_fn)

        print "Success"
        return name_trie_list, ip6_trie_list


def build_map(name_trie_list, ip6_trie_list, filename='../records/aaaa.csv'):
    with open(filename, 'rb') as f:
        print f
        reader = DictReader(f)
        current = None
        current_host = None
        count = 0
        i = 0

        triplets = []
        if len(ip6_trie_list) == 1:
            ip6_indexes = ip6_trie_list[0]
            name_indexes = name_trie_list[0]

        for row in reader:
            i += 1
            if i % 10000000 == 0:
                print i

            prev = current
            current = row[reader.fieldnames[2]]
            # print prev, current
            prev_host = current_host
            current_host = row[reader.fieldnames[0]]
            # print prev_host, current_host
            if prev_host != current_host and prev_host is not None:
                triplets.append((name_indexes.key_id(unicode(prev_host)),
                                 ip6_indexes.key_id(unicode(prev)),
                                 count))

                # print prev_host, prev, count
                # keys.append(prev_host)
                # values.append((ip6_indexes.key_id(unicode(prev)), count))
                count = 1
            else:
                if prev != current and prev is not None:
                    triplets.append((name_indexes.key_id(unicode(prev_host)),
                                     ip6_indexes.key_id(unicode(prev)),
                                     count))

                    # print prev_host, prev, count
                    # keys.append(prev_host)
                    # values.append((ip6_indexes.key_id(unicode(prev)), count))
                    count = 1
                else:
                    count += 1

        out_file = open(filename.replace('.csv', '_triplets_all.pkl'), 'wb')
        Pickle.dump(triplets, out_file)
        out_file.close()

# name_trie_list, ip6_trie_list = index_ip6address_4_aaaa()
# # print dictionary['::ffff:74.117.221.143']
# build_map(name_trie_list, ip6_trie_list)
