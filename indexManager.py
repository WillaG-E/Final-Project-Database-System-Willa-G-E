#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Use and pass the record index into the Hash Table and B+ Tree

from hashTable import HashTable, hashFNV_1a
from bPlusTree import BPlusTree

class IndexManager:
    def __init__(self, searchableFields):
        self.searchableFields = searchableFields
        self.hashTables = {
            f: HashTable(hashFunction = hashFNV_1a, size = 20000) 
            for f in searchableFields
        }
        self.bplusIndices = {}
    
    def add_hash_record(self, record, recordIndex):
        for field, hash in self.hashTables.items():
            hash.add(record.getField(field), recordIndex)

    def create_bplus_index(self, field, records):
        sortedPairs = [(self.parse_key(field, r.getField(field)), i)
                        for i, r in enumerate(records) if r is not None]
        sortedPairs = [pair for pair in sortedPairs if pair[0] is not None]
        sortedPairs.sort(key = lambda x: str(x[0]))
        tree = BPlusTree(maxDegree = 100)
        tree.bulkLoad(sortedPairs)
        self.bplusIndices[field] = tree

    def delete_all(self, record, recordIndex):
        #deletes from the hash table
        for field, hash in self.hashTables.items():
            hash.remove(record.getField(field), recordIndex)

        #deletes from the b+ trees; if the index exists
        for field, bPlusTree in self.bplusIndices.items():
            bPlusTree.delete(record.getField(field), recordIndex)

    def parse_key(self, field, value):
        numeric_fields = ["rating", "box_office_revenue"]

        if field == "box_office_revenue" and isinstance(value, str):
            import re
            try:
                return float(re.sub(r'[$,]', '', value))
            except ValueError:
                return None
            
        return value