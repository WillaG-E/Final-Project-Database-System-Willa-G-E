#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: B+ Tree Index Structure

class DataItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value #to use when there is duplicate keys

    def __str__(self):
        return str(self.key)
    
    def _repr__(self):
        return str(self.key)
    
class Bucket:
    def __init__(self, maxDegree):
        self.keys = [] #list of DataItem (leaf) or keys (internal node)
        self.links = [] #links to child nodes (internal) or list of record indices (leaf)
        self.parent = None
        self.is_leaf = True
        self.next = None #pointer, pointing to the next leaf node
        self.prev = None #pointer, pointing to the previous leaf node
        self.maxDegree = maxDegree

    def __str__(self):
        return str(self.keys)
        
    def __repr__(self):
        return str(self.keys)
    
class BucketNode(Bucket):
    def add(self, item, leftLink = None):
        targetIndex = 0
        while (targetIndex < len(self.keys) and item.key >= self.keys[targetIndex].key):
            targetIndex += 1
        
        if (self.is_leaf):
            if (targetIndex > 0 and self.keys[targetIndex - 1].key == item.key):
                self.keys.insert(targetIndex, item)
            else:
                self.keys.insert(targetIndex, item)
            return len(self.keys)
        else:
            self.keys.insert(targetIndex, item)
            self.links.insert(targetIndex, leftLink)
            return len(self.keys)
        
    def remove(self, key):
        i = 0
        while i < len(self.keys):
            if (self.keys[i] == key):
                self.keys.pop(i)
                return True
            i += 1
        return False
    
class BPlusTree:
    def __init__(self, maxDegree, fieldName = ""):
        self.root = None
        self.maxDegree = maxDegree
        self.fieldName = fieldName

    def add(self, key, value):
        data = DataItem(key, value)
        if (self.root == None):
            self.root = BucketNode(self.maxDegree)
            self.root.is_leaf = True
            self.root.keys.append(data)
            return
        
        node = self.root
        while (node.is_leaf == None):
            i = 0
            while (i < len(node.keys) and key >= node.keys[i].key):
                i += 1
            node = node.links[i]
        node.add(data)
        if (len(node.keys) > self.maxDegree):
            self.split_leaf_node(node)
        
    def split_leaf_node(self, node):
        middle = self.maxDegree // 2
        leftNode = BucketNode(self.maxDegree)
        leftNode.is_leaf = True
        leftNode.keys = node.keys[:middle]

        promoteKey = node.keys[middle]
        node.keys = node.keys[middle:]

        leftNode.next = node
        leftNode.prev = node.prev
        if (node.prev):
            node.prev.next = leftNode
        node.prev = leftNode

        if (node.parent == None):
            self.root = BucketNode(self.maxDegree)
            self.root.is_leaf = False
            self.root.keys = [promoteKey]
            self.root.links = [leftNode, node]
            leftNode.parent = self.root
            node.parent = self.root
            return
        
        splitIndex = node.parent.add(promoteKey, leftNode)
        leftNode.parent = node.parent

        #check if the parent needs to be split
        if (len(node.parent.keys) > self.maxDegree):
            self.split_internal_node(node.parent)

    def split_internal_node(self, node):
        middle = self.maxDegree // 2
        leftNode = BucketNode(self.maxDegree)
        leftNode.is_leaf = False

        leftNode.keys = node.keys[:middle]
        leftNode.links = node.links[:middle + 1]
        for child in leftNode.links:
            child.parent = leftNode
        
        promote = node.keys[middle]

        node.keys = node.keys[middle + 1:]
        node.links = node.links[middle + 1:]

        #handling the root split
        if (node.parent == None):
            self.root = BucketNode(self.maxDegree)
            self.root.is_leaf = False
            self.root.keys = [promote]
            self.root.links = [leftNode, node]
            leftNode.parent = self.root
            node.parent = self.root
            return
        
        splitIndex = node.parent.add(promote, leftNode)
        leftNode.parent = node.parent

        if (len(node.parent.keys) > self.maxDegree):
            self.split_internal_node(node.parent)

    #pasted code from BPlusTree homework assignment
    def fix_leaf_bucket(self, node):
        if node == self.root:
            return
        left, right, index = self.get_siblings(node)
        if self.valid_steal(left):
            self.leaf_steal(node, 'left')
        elif self.valid_steal(right):
            self.leaf_steal(node, 'right')
        elif left:
            self.leaf_merge(left, node)
        else:
            self.leaf_merge(node, right)

    def fix_internal_bucket(self, node):
        if node == self.root:
            return
        left, right, index = self.get_siblings(node)
        if self.valid_steal(left):
            self.internal_steal(node, 'left')
        elif self.valid_steal(right):
            self.internal_steal(node, 'right')
        elif left:
            self.internal_merge(left, node)
        else:
            self.internal_merge(node, right)

    def get_siblings(self, node):
        left, right = None, None
        index = 0
        while index < len(node.parent.links) and node.parent.links[index] != node:
            index += 1
        if index > 0:
            left = node.parent.links[index - 1]
        if index < len(node.parent.links) - 1:
            right = node.parent.links[index + 1]
        return left, right, index

    def valid_steal(self, node):
        if node is None:
            return False
        if len(node.keys) <= (self.maxdegree - 1) // 2:
            return False
        return True

    def leaf_steal(self, node, direction):
        parent = node.parent
        left, right, index = self.get_siblings(node)
        if direction == 'left':
            sibling = left
            borrowed = sibling.keys.pop(-1)
            node.keys.insert(0, borrowed)
            parent.keys[index - 1] = node.keys[0]
        else:
            sibling = right
            borrowed = sibling.keys.pop(0)
            node.keys.append(borrowed)
            parent.keys[index] = sibling.keys[0]

    def internal_steal(self, node, direction):
        parent = node.parent
        left, right, index = self.get_siblings(node)
        if direction == 'left':
            sibling = left
            borrow_key = sibling.keys.pop(-1)
            borrow_link = sibling.links.pop(-1)
            node.keys.insert(0, parent.keys[index - 1])
            node.links.insert(0, borrow_link)
            borrow_link.parent = node
            parent.keys[index - 1] = borrow_key
        else:
            sibling = right
            borrow_key = sibling.keys.pop(0)
            borrow_link = sibling.links.pop(0)
            node.keys.append(parent.keys[index])
            node.links.append(borrow_link)
            borrow_link.parent = node
            parent.keys[index] = borrow_key

    def leaf_merge(self, leftNode, rightNode):
        leftNode.keys.extend(rightNode.keys)
        leftNode.next = rightNode.next
        if rightNode.next:
            rightNode.next.prev = leftNode
        parent = leftNode.parent
        idx = 0
        while idx < len(parent.links) and parent.links[idx] != leftNode:
            idx += 1
        parent.keys.pop(idx)
        parent.links.pop(idx + 1)
        if parent != self.root and len(parent.keys) < (self.maxdegree - 1) // 2:
            self.fix_internal_bucket(parent)

    def internal_merge(self, leftNode, rightNode):
        parent = leftNode.parent
        idx = 0
        while idx < len(parent.links) and parent.links[idx] != leftNode:
            idx += 1
        leftNode.keys.append(parent.keys[idx])
        leftNode.keys.extend(rightNode.keys)
        leftNode.links.extend(rightNode.links)
        for child in rightNode.links:
            child.parent = leftNode
        parent.keys.pop(idx)
        parent.links.pop(idx + 1)
        if parent == self.root and len(parent.keys) == 0:
            self.root = leftNode
            leftNode.parent = None
        elif parent != self.root and len(parent.keys) < (self.maxdegree - 1) // 2:
            self.fix_internal_bucket(parent)


    def findLeaf(self, key):
        #helper function to help navigate from the root to the correct leaf node for a given key
        node = self.root
        if (node == None):
            return
        while (node != None):
            i = 0
            while (i < len(node.keys) and key >= node.keys[i].key):
                i += 1
                #make sure that links exist before accessing links
                if (node.is_leaf):
                    return node
                if i < len(node.links):
                    node = node.links[i]
                else:
                    return None
        return None
    
    def insert(self, key, recordIndex):
        self.add(key, recordIndex)
    
    def bulkLoad(self, sortedPairs):
        if (sortedPairs == None):
            return
        
        leafNodes = []
        currentLeaf = BucketNode(self.maxDegree)
        currentLeaf.is_leaf = True

        for i, (key,index) in enumerate(sortedPairs):
            dataItem = DataItem(key, index)
            currentLeaf.keys.append(dataItem)

            if (len(currentLeaf.keys) >= self.maxDegree):
                leafNodes.append(currentLeaf)
                nextLeaf = BucketNode(self.maxDegree)
                nextLeaf.is_leaf = True
                currentLeaf.next = nextLeaf
                nextLeaf.prev = currentLeaf
                currentLeaf = nextLeaf

            if (currentLeaf.keys):
                leafNodes.append(currentLeaf)

                nodesBuild = leafNodes
            while (len(nodesBuild) > 1):
                nodesNextLevel = []
                newParent = BucketNode(self.maxDegree)
                newParent.is_leaf = False

                for i, child in enumerate(nodesBuild):
                    if (i > 0):
                        promoteKeyValue = child.leys[0]
                        promoteData = DataItem(promoteKeyValue.key, None)

                        #insert into parent
                        newParent.keys.append(promoteData)

                        #link to the previous node
                        newParent.links.append(nodesBuild[i - 1])
                        nodesBuild[i - 1].parent = newParent

                    if (i == len(nodesBuild) - 1):
                        newParent.links.append(child)
                        child.parent = newParent

                    #check for a parent split
                    if (len(newParent.keys) >= self.maxDegree):
                        #implement an internal split similar to split_internal_node
                        pass
                if (len(nodesBuild) > 1):
                    nodesNextLevel.append(newParent)
                    nodesBuild = nodesNextLevel
            
            if (leafNodes):
                self.root = leafNodes[0].parent if leafNodes[0].parent else leafNodes[0]

    def delete(self, key, recordIndex):
        node = self.findLeaf(key)
        if (node == None):
            return
        
        targetIndex = -1
        #find the specific DataItem
        for i, item in enumerate(node.keys):
            if (item.key == key and item.value == recordIndex):
                targetIndex = i
                break
        if (targetIndex != -1):
            node.keys.pop(targetIndex)

            minKeys = (self.maxDegree - 1) // 2
            if (node != self.root and len(node.keys) < minKeys):
                self.fix_leaf_bucket(node)

    def rangeSearch(self, low = None, high = None):
        allIndices = set()
        
        startKey = low if low != None else -float('inf')
        currentNode = self.findLeaf(startKey)

        if (currentNode == None):
            return []
        
        while (currentNode != None):
            for item in currentNode.keys:
                key = item.key
                index = item.value

                if (low != None and key < low):
                    continue

                if (high != None and key > high):
                    return list(allIndices)
                
                allIndices.add(index)

            currentNode = currentNode.next
        return list(allIndices)