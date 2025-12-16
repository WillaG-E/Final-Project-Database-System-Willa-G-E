#Author: Willa Galipeau-Eldridge
#Date: 12/14/2025
#Purpose: 

import csv

class Database:
    def __init__(self, searchableFields, initialIndexedField):
        self
    
    def load_csv(self, path):
        records = []

        with open(path) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                record = records(row[0], row[1], row[2], row[3], row[4])
                self.records.append(record)

