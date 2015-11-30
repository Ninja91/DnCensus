#!/usr/bin/python

__author__ = 'Nitin'

import marisa_trie as mt
import csv
import os.path
import marshal as Pickle
import threading
import commons
import preprocessing as pp

DEBUG_MODE = False
TARGET_INDEX_FILE = '_target_index.marisa'
NAME_INDEX_FILE = '_name_index.marisa'
COMBINED_NAME_INDEX_FILE = '../records/combined_name_indexes.marisa'
COMBINED_TARGET_INDEX_FILE = '../records/combined_target_indexes.marisa'

class Index_Result:
    def __init__(self):
        self.trie_tuple_dict = dict()
        self.all_indexing_trie_tuple = tuple()
        self.writer_threads = list()


def index_field_in_file(reader_obj, field_num):
    final_index_list = list()
    temp_list = list()
    i = 1
    for row in reader_obj:
        if DEBUG_MODE and i == 100:
            break
        if i % 10000000 == 0:
            print i
            temp_list = list(set(temp_list))
            temp_list[0:0] = final_index_list
            final_index_list = temp_list
            temp_list = list()

        # print row
        temp_list.append(row[field_num])
        i += 1
    temp_list = list(set(temp_list))
    temp_list[0:0] = final_index_list
    final_index_list = temp_list

    return final_index_list


def save_trie_in_file(trie, filename):
    trie.save(filename)


def trie_saver(indexing_result, trie, filename):
    thread = threading.Thread(target=save_trie_in_file, args=(trie, filename))
    thread.start()
    indexing_result.writer_threads.append(thread)


def create_combined_index(indexing_result):
    if os.path.isfile(COMBINED_NAME_INDEX_FILE) and os.path.isfile(COMBINED_TARGET_INDEX_FILE):
        name_trie = mt.Trie().load(COMBINED_NAME_INDEX_FILE)
        target_trie = mt.Trie().load(COMBINED_TARGET_INDEX_FILE)
        print 'Loaded', COMBINED_NAME_INDEX_FILE, COMBINED_TARGET_INDEX_FILE
    else:
        name_list = list()
        target_list = list()

        for trie_tuple in indexing_result.trie_tuple_dict.itervalues():
            name_list[0:0] = trie_tuple[0].keys()
        name_trie = mt.Trie(name_list)

        for trie_tuple in indexing_result.trie_tuple_dict.itervalues():
            target_list[0:0] = trie_tuple[1].keys()
        target_trie = mt.Trie(target_list)

        trie_saver(indexing_result, name_trie, COMBINED_NAME_INDEX_FILE)
        trie_saver(indexing_result, target_trie, COMBINED_TARGET_INDEX_FILE)

    if DEBUG_MODE is True:
        print name_list
        print target_list

    indexing_result.all_indexing_trie_tuple = (name_trie, target_trie)


    print 'Combined'
    print 'ncols =', len(target_trie)
    print 'nrows =', len(name_trie)
    print '\n'


def index_field(filenames=['../records/aaaa.csv', '../records/a.csv']):
    indexing_result = Index_Result()
    for filename in filenames:
        print filename
        target_index_fn = filename.replace('.csv', TARGET_INDEX_FILE)
        name_index_fn = filename.replace('.csv', NAME_INDEX_FILE)

        if os.path.isfile(target_index_fn) and os.path.isfile(name_index_fn):
            name_trie = mt.Trie().load(name_index_fn)
            target_trie = mt.Trie().load(target_index_fn)
            print 'Loaded', name_index_fn, target_index_fn
        else:
            with open(filename, 'rb') as f:
                reader = csv.reader(f)
                next(reader)
                # print reader
                file_name_list = index_field_in_file(reader, 0)

            with open(filename, 'rb') as f:
                reader = csv.reader(f)
                next(reader)

                file_target_list = index_field_in_file(reader, 2)

            target_trie = mt.Trie(file_target_list)
            name_trie = mt.Trie(file_name_list)

            trie_saver(indexing_result, name_trie, name_index_fn)
            trie_saver(indexing_result, target_trie, target_index_fn)

        indexing_result.trie_tuple_dict[filename] = (name_trie, target_trie)

        print filename
        print 'ncols =', len(target_trie)
        print 'nrows =', len(name_trie)
        print '\n'

    create_combined_index(indexing_result)
    return indexing_result


# def build_map(filenames=['../records/aaaa.csv', '../records/cname.csv', '../records/dname.csv', '../records/a.csv'],
#               indexing_result):
#     all_name_index_trie = indexing_result.all_indexing_trie_tuple(0)
#     all_target_index_trie = indexing_result.all_indexing_trie_tuple(1)
#     for filename in filenames:


indexing_result = index_field(['../records/aaaa.csv', '../records/cname.csv', '../records/dname.csv', '../records/a.csv'])
all_name_index, all_target_index = indexing_result.all_indexing_trie_tuple
for filename in [ '../records/cname.csv', '../records/aaaa.csv', '../records/dname.csv', '../records/a.csv']:
    pp.build_map(all_name_index, all_target_index, filename)


