#Author: Willa Galipeau-Eldridge
#Date: 12/11/2025
#Purpose: Hash Table

class HashTable:
    def __init__(self, size, hashFunction, fieldName = ""):
        self.size = size
        self.hashTable = [None] * size
        self.hashFunction = hashFunction
        self.fieldName = fieldName

    def add(self, key, item):
        #Make sure that there is a key; return otherwise
        if (key == None):
            return
        
        #modify the index value by the hash table length
        index = self.hashTable[index] % self.size

        #insert a data item into the hash table
        #check to see if there is already an index; if not then append that item
        if (self.hashTable[index] == None):
            self.hashTable[index] = [item]
        else:
            self.hashTable[index].append(item)

    def bulkAdd(self, items):
        for item in items:
            key = item.keys[self.fieldName]
            self.add(key, item)

    def search(self, key):
        index = self.hashFunction(key) % self.size
        bucket = self.hashTable[index]
        if not bucket:
            return []
        results = []
        for item in bucket:
            if (item.keys[self.fieldName] == key):
                results.append(item)
        return results

#Hash Function - using most consistent from FNV-1a
#pasted in from hash tables; HW5 - Hash Something Out
def hashFNV_1a(stringData):
    #if stringData is none return and don't continue
    if not stringData:
        return 0
    
    #FNV-1a algorithm constants
    prime = 16777619
    offsetBasis = 2166136261

    key = offsetBasis
    for character in stringData:
        key ^= ord(character)
        key = (key * prime) & 0xffffffff
    return key