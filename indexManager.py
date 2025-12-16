#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Use and pass the record index into the Hash Table and B+ Tree

from hashTable import HashTable, hashFNV_1a
from bPlusTree import BPlusTree
from records import Record

class IndexManager:
    def __init__(self, searchableFields):
        self.searchableFields = searchableFields
        self.hashTables = {}
        self.bplusIndices = {}
        for field in searchableFields:
            self.hashTables[field] = HashTable(hashFunction = hashFNV_1a, size = 20000, fieldName = field)
    
    def add_hash_record(self, record, recordIndex):
        for field, hash in self.hashTables.items():
            key = record.getField(field)
            hash.add(key, recordIndex)

    def create_bplus_index(self, field, record_with_indices):
        sortedPairs = sorted([(r.getField(field), index) for r, index in record_with_indices], key = lambda x: x[0])
        tree = BPlusTree(maxDegree = 100, fieldName = field)
        tree.bulkLoad(sortedPairs)
        self.bplusIndices[field] = tree

    def delete_all(self, record, recordIndex):
        for field, hash in self.hashTables.items():
            key = record.getField(field)
            hash.delete(key, recordIndex)

        for field, tree in self.bplusIndices.items():
            key = record.getField(field)
            tree.delete(key, recordIndex)
