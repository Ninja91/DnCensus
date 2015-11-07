__author__ = 'Nitin'


import preprocessing as pp
import sys


def create_map():
    if len(sys.argv) == 1:
        name_trie_list, ip6_trie_list = pp.index_ip6address_4_aaaa()
        pp.build_map(name_trie_list, ip6_trie_list)
    else:
        name_trie_list, ip6_trie_list = pp.index_ip6address_4_aaaa(sys.argv[1])
        pp.build_map(name_trie_list, ip6_trie_list, sys.argv[1])

if __name__ == "__main__":
    create_map()