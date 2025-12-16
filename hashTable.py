#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: Hash Table logic

class HashTable:
    def __init__(self, size, hashFunction):
        self.size = size
        self.hashTable = [[] for _ in range(size)]
        self.hashFunction = hashFunction

    def add(self, key, recordIndex):
        #Make sure that there is a key; return otherwise
        if key is None:
            return
        #modify the index value by the hash table length
        index = self.hashFunction(str(key)) % self.size
        self.hashTable[index].append((key, recordIndex))

    def search(self, key):
         #Make sure that there is a key; return otherwise
        if key is None:
            return
        index = self.hashFunction(str(key)) % self.size
        return [ri for k, ri in self.hashTable[index] if str(k) == str(key)]

    def remove(self, key, recordIndex):
        if (key == None):
            return
        
        index = self.hashFunction(str(key)) % self.size
        bucket = self.hashTable[index]

        self.hashTable[index] = [
            (k, ri) for k, ri in bucket
            if not (str(k) == str(key) and ri == recordIndex)
        ]

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