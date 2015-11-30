#!/usr/bin/python

__author__ = 'Nitin'

import threading
import marisa_trie as mt
import csv
import os.path
import marshal as Pickle
from backports import lzma as lz

IP6_INDEX_FILE = '_ip6_index.marisa'
NAME_INDEX_FILE = '_name_index.marisa'


def build_map(all_name_index_trie, all_target_index_trie, filename='../records/aaaa.csv'):
    filename = filename.replace('.csv', '.smat')
    if os.path.isfile(filename):
        print filename
        print 'nnz = ', sum(1 for line in open(filename))
        return None

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        next(reader)
        current_target = None
        current_name = None
        count = 0
        i = 0

        triplets = list()

        for row in reader:
            i += 1
            # if i == 11:
            #     break
            if i % 10000000 == 0:
                print i

            prev_name, prev_target = current_name, current_target
            current_name, current_target = row[0], row[2]

            if prev_name != current_name and prev_name is not None:
                triplets.append((all_name_index_trie.key_id(unicode(prev_name)),
                                 all_target_index_trie.key_id(unicode(prev_target)),
                                 count))

                # print prev_host, prev, count
                # keys.append(prev_host)
                # values.append((ip6_indexes.key_id(unicode(prev)), count))
                count = 1
            else:
                if prev_target != current_target and prev_target is not None:
                    triplets.append((all_name_index_trie.key_id(unicode(prev_name)),
                                     all_target_index_trie.key_id(unicode(prev_target)),
                                     count))

                    # print prev_host, prev, count
                    # keys.append(prev_host)
                    # values.append((ip6_indexes.key_id(unicode(prev)), count))
                    count = 1
                else:
                    count += 1
        triplets.append((all_name_index_trie.key_id(unicode(prev_name)),
                         all_target_index_trie.key_id(unicode(prev_target)),
                         count))
        print filename
        print 'nnz = ', len(triplets)
        out_filename = filename.replace('.csv', '.smat')
        t = threading.Thread(target=store_in_smat, args=(triplets, out_filename))
        t.start()
        return t
        # store_in_smat(triplets, out_file)
        # Pickle.dump(triplets, out_file)
        # out_file.close()


def store_in_smat(triplets, out_filename):
    with open(out_filename, 'wb') as f:
        for triplet in triplets:
            f.write(str(triplet[0]) + ' ' + str(triplet[1]) + ' ' + str(triplet[2]) + '\n')
# all_name_index_trie, all_target_index_trie = index_ip6address_4_aaaa()
# # print dictionary['::ffff:74.117.221.143']
# build_map(all_name_index_trie, all_target_index_trie)
