#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Stores data for fileds using CSV headers

class Record:
    FIELD_NAMES = []

    def __init__(self, rowData):
        self.data = {}
        for i, fieldName in enumerate(self.FIELD_NAMES):
            self.data[fieldName] = rowData[i]

    def getField(self, fieldName):
        return self.data.get(fieldName)
    
    def csvRow(self):
        return [str(self.data[field]) for field in self.FIELD_NAMES]
    
    def __repr__(self):
        return str(self.data)