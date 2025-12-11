#Author: Willa Galipeau-Eldridge
#Date:
#Purpose:




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