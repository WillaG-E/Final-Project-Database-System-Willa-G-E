#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: 

from recordStorage import Storage
from indexManager import IndexManager
from records import Record
import csv

class Database:
    def __init__(self, searchableFields):
        self.storage = Storage()
        self.indexManager = IndexManager(searchableFields)
    
    def load_csv(self, path):
        self.storage.records = []
        self.indexManager = IndexManager(self.indexManager.searchableFields)

        with open(path) as f:
            reader = csv.reader(f)
            header = next(reader)
            Record.FIELD_NAMES = header
            
            for index, row in enumerate(reader):
                rec = Record(row)
                self.storage.records.append(rec)

        for index, rec in enumerate(self.storage.records):
            self.indexManager.add_hash_record(rec, index)

    def create_index(self, field):
        records_with_indices = [(r, i) for i, r in enumerate(self.storage.records) if r != None]
        self.indexManager.create_bplus_index(field, records_with_indices)

    def get_record_indices(self, recordIndices):
        records = []
        for i in recordIndices:
            if (i < len(self.storage.records)):
                record = self.storage.records[i]
                if (record != None):
                    records.append(record)
        return records
    
    def exact_search(self, field, value):
        hash = self.indexManager.hashTables[field]
        recordIndices = hash.search(value)
        return self.get_record_indices(recordIndices)
    
    def range_search(self, field, low, high):
        if field not in self.indexManager.bplusIndices:
            raise Exception("Field is not indexed.")
        
        tree = self.indexManager.bplusIndices[field]
        recordIndices = tree.range_search(low, high)
        return self.get_record_indices(recordIndices)
    
    def delete_records(self, records):
        for r in records:
            try:
                recordIndex = self.storage.records.index(r)
            except ValueError:
                continue

            self.indexManager.delete_all(r, recordIndex)
            self.storage.deleteRecords([r])