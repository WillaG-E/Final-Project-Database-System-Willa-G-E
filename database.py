#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Load the CSV file and hold the database logic

from recordStorage import Storage
from indexManager import IndexManager
from records import Record
import csv

class Database:
    def __init__(self, searchableFields):
        self.storage = Storage()
        self.indexManager = IndexManager(searchableFields)
    
    def load_csv(self, file):
        self.storage.records = []
        self.indexManager = IndexManager(self.indexManager.searchableFields)

        with open(file, 'r', newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            Record.FIELD_NAMES = header

            for row in reader:
                self.storage.records.append(Record(row))

        for index, rec in enumerate(self.storage.records):
            self.indexManager.add_hash_record(rec, index)
        
        print(f"Loaded {len(self.storage.records)} records.")

    def create_index(self, field):
        self.indexManager.create_bplus_index(field, self.storage.records)
    
    def exact_search(self, field, value):
        if field not in self.indexManager.hashTables:
            print(f"Errot: Field '{field}' is not a searchable field.")
            return []
        indices = self.indexManager.hashTables[field].search(value)
        return [self.storage.records[i] for i in indices if i < len(self.storage.records) and self.storage.records[i] is not None]
    
    def range_search(self, field, low, high):
        if field not in self.indexManager.bplusIndices:
            print(f"Error: Index for field '{field}' does not exist. Please create it first.")
            return []
        
        tree = self.indexManager.bplusIndices[field]
        def clean_bounds(val):
            try:
                import re
                return float(re.sub(r'[$,]', '', str(val)))
            except:
                return val
            
        low = clean_bounds(low) if low != "" else None
        high = clean_bounds(high) if high != "" else None
        indices = tree.rangeSearch(low, high)
        return [self.storage.records[i] for i in indices 
                if i < len(self.storage.records) and self.storage.records[i] is not None]
    
    def delete_records(self, recordsDelete):
        deletedCount = 0
        for r in recordsDelete:
            try:
                recordIndex = self.storage.records.index(r)
                self.indexManager.delete_all(r, recordIndex)
                self.storage.records[recordIndex] = None
                deletedCount += 1
            except ValueError:
                continue
        if deletedCount > 0:
            self.exportModifiedDatabase("MODIFIED_DATABASE.csv")

        return deletedCount
    
    def exportModifiedDatabase(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(Record.FIELD_NAMES)
            for r in self.storage.records:
                if r is not None:
                    writer.writerow(r.csvRow())