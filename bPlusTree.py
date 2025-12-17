#Author: Willa Galipeau-Eldridge
#Date: 12/16/2025
#Purpose: B+ Tree Index Structure

class DataItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value #to use when there is duplicate keys
    
    def __repr__(self):
        return f"({self.key}:{self.value})"

class Bucket:
    def __init__(self, maxDegree, is_leaf=False):
        self.keys = [] #list of DataItem (leaf) or keys (internal node)
        self.children = [] #links to child nodes (internal) or list of record indices (leaf)
        self.parent = None
        self.is_leaf = is_leaf
        self.next = None #pointer, pointing to the next leaf node
        self.prev = None #pointer, pointing to the previous leaf node
        self.maxDegree = maxDegree
    
class BucketNode(Bucket):
    def add(self, item, leftLink = None):
        targetIndex = 0

        if (self.is_leaf):
            #find the point to insert
            while (targetIndex < len(self.keys) and item.key > self.keys[targetIndex].key):
                targetIndex += 1
            
                #handling duplicate keys
                if (targetIndex < len(self.keys) and item.key == self.keys[targetIndex].key):
                    while (targetIndex < len(self.keys) and item.key == self.keys[targetIndex].key):
                        targetIndex += 1
                self.keys.insert(targetIndex, item)
                return len(self.keys)
        else:
            while (targetIndex < len(self.keys) and item.key >= self.keys[targetIndex.key]):
                targetIndex += 1
            self.keys.insert(targetIndex, item)
            if leftLink:
                self.children.insert(targetIndex, leftLink)
            return len(self.keys)
        
class BPlusTree:
    def __init__(self, maxDegree):
        self.root = None
        self.maxDegree = maxDegree

    def add(self, key, value):
        data = DataItem(key, value)
        if (self.root == None):
            self.root = BucketNode(self.maxDegree, is_leaf = True)
            self.root.keys.append(data)
            return
        
        node = self.root
        while (not node.is_leaf):
            i = 0
            while (i < len(node.keys) and key >= node.keys[i].key):
                i += 1
            node = node.children[i]
        node.add(data)
        if (len(node.keys) > self.maxDegree):
            self.split_leaf_node(node)
        
    def split_leaf_node(self, node):
        middle = (self.maxDegree + 1) // 2
        leftNode = BucketNode(self.maxDegree, is_leaf = True)
        leftNode.keys = node.keys[:middle]

        promoteKey = node.keys[middle].key
        promoteData = DataItem(promoteKey, None)

        node.keys = node.keys[middle:]

        leftNode.next = node
        leftNode.prev = node.prev
        if (node.prev):
            node.prev.next = leftNode
        node.prev = leftNode

        if (node.parent == None):
            self.root = BucketNode(self.maxDegree, is_leaf = False)
            self.root.keys = [promoteData]
            self.root.children = [leftNode, node]
            leftNode.parent = self.root
            node.parent = self.root
            return
        
        node.parent.add(promoteKey, leftNode)
        leftNode.parent = node.parent

        #check if the parent needs to be split
        if (len(node.parent.keys) > self.maxDegree):
            self.split_internal_node(node.parent)

    def split_internal_node(self, node):
        middle = self.maxDegree // 2
        leftNode = BucketNode(self.maxDegree, is_leaf = False)

        leftNode.keys = node.keys[:middle]
        leftNode.children = node.links[:middle + 1]
        for child in leftNode.children:
            child.parent = leftNode
        
        promote = node.keys[middle]

        node.keys = node.keys[middle + 1:]
        node.children = node.children[middle + 1:]

        #handling the root split
        if (node.parent == None):
            self.root = BucketNode(self.maxDegree, is_leaf = False)
            self.root.keys = [promote]
            self.root.children = [leftNode, node]
            leftNode.parent = self.root
            node.parent = self.root
            return
        
        node.parent.add(promote, leftNode)
        leftNode.parent = node.parent

        if (len(node.parent.keys) > self.maxDegree):
            self.split_internal_node(node.parent)

    def findLeaf(self, key):
        #helper function to help navigate from the root to the correct leaf node for a given key
        node = self.root
        if (node == None):
            return None
        while (not node.is_leaf):
            i = 0
            while (i < len(node.keys) and key >= node.keys[i].key):
                i += 1
                if i < len(node.children):
                    node = node.children[i]
                else:
                    return None
        return node
    
    def bulkLoad(self, sortedPairs):
        if not sortedPairs:
            self.root = None
            return
        
        leafNodes = []
        currentLeaf = BucketNode(self.maxDegree, is_leaf = True)

        for key, index in sortedPairs:
            dataItem = DataItem(key, index)
            currentLeaf.keys.append(dataItem)

            if (len(currentLeaf.keys) >= self.maxDegree):
                leafNodes.append(currentLeaf)
                nextLeaf = BucketNode(self.maxDegree, is_leaf = True)
                currentLeaf.next = nextLeaf
                nextLeaf.prev = currentLeaf
                currentLeaf = nextLeaf

        if (currentLeaf.keys and currentLeaf not in leafNodes):
            leafNodes.append(currentLeaf)

        if not leafNodes:
            self.root = None
            return
            
        nodesBuild = leafNodes
        while (len(nodesBuild) > 1):
            nodesNextLevel = []
            i = 0
            while (i < len(nodesBuild)):
                parent = BucketNode(self.maxDegree, is_leaf = False)

                parent.children.append(nodesBuild[i])
                nodesBuild[i].parent = parent

                j = i + 1
                while (j < len(nodesBuild) and len(parent.keys) < self.maxDegree):
                    promoteKey = nodesBuild[j].keys[0].key
                    parent.keys.append(DataItem(promoteKey, None))
                    parent.children.append(nodesBuild[j])
                    nodesBuild[j].parent = parent
                    j += 1
                    
                nodesNextLevel.append(parent)
                i = j

            nodesBuild = nodesNextLevel
        self.root = nodesBuild[0]

    def delete(self, key, recordIndex):
        node = self.findLeaf(key)
        if (node == None):
            return
        
        targetIndex = -1
        #find the specific DataItem
        for i, item in enumerate(node.keys):
            if (str(item.key) == str(key) and item.value == recordIndex):
                targetIndex = i
                break
        if (targetIndex != -1):
            smallest_key = (targetIndex == 0) and (node.prev is None or node.prev.keys[-1].key != key)
            node.keys.pop(targetIndex)

            if smallest_key and node.keys:
                parent = node.parent
                while parent:
                    try:
                        childIndex = parent.children.index(node)
                        if childIndex > 0:
                            parent.keys[childIndex - 1] = DataItem(node.keys[0].key, None)
                            break
                        else:
                            pass
                    except ValueError:
                        break
                    parent = parent.parent
            minKeys = self.maxDegree // 2
            if (node != self.root and len(node.keys) < minKeys):
                self.fix_leaf_bucket(node)

    def rangeSearch(self, low = None, high = None):
        allIndices = set()
        
        startKey = low if low is not None else -float('inf')
        currentNode = self.findLeaf(startKey)

        if (currentNode == None):
            return []
        
        while (currentNode is not None):
            for item in currentNode.keys:
                key = item.key
                index = item.value

                if (high is not None and key > high):
                    return list(allIndices)

                if (low is not None or key >= low):
                    allIndices.add(index)
                
                allIndices.add(index)

            currentNode = currentNode.next
        return list(allIndices)
    
        #pasted code from BPlusTree homework assignment
    def fix_leaf_bucket(self, node):
        if node == self.root:
            if not node.keys:
                self.root = None
            return
        left, right = self.get_siblings(node)
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
            if not node.keys:
                self.root = None
            return
        left, right = self.get_siblings(node)
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
