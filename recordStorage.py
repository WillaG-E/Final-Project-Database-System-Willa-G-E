#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Primary memory storage of records

class Storage:
    def __init__(self):
        self.records = []

    def bulkLoad(self, records):
        self.records = records

    def deleteRecords(self, recordList):
        deletedCount = 0
        for r in recordList:
            try:
                recordIndex = self.records.index(r)
                self.records[recordIndex] = None
                deletedCount += 1
            except ValueError:
                print("Record not found.")

        return deletedCount
