from operator import attrgetter


leafEnd = -1


class Node:
    

    def __init__(self, leaf):
        
        self.children = {}
        self.leaf = leaf
        self.suffixIndex = None
        self.start = None
        self.end = None
        self.suffixLink = None

    def __eq__(self, node):
        atg = attrgetter('start', 'end', 'suffixIndex')
        return atg(self) == atg(node)

    def __ne__(self, node):
        atg = attrgetter('start', 'end', 'suffixIndex')
        return atg(self) != atg(node)

    def __getattribute__(self, name):
        if name == 'end':
            if self.leaf:
                return leafEnd
        return super(Node, self).__getattribute__(name)


class SuffixTree:
   

    def __init__(self, data):
        self._string = data
        self.lastNewNode = None
        self.activeNode = None
        self.activeEdge = -1
        self.activeLength = 0
        self.remainingSuffixCount = 0
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1  
        self.root = None

    def edge_length(self, node):
        return node.end - node.start + 1

    def walk_down(self, current_node):
        length = self.edge_length(current_node)
        if (self.activeLength >= length):
            self.activeEdge += length
            self.activeLength -= length
            self.activeNode = current_node
            return True
        return False

    def new_node(self, start, end=None, leaf=False):
        node = Node(leaf)
        node.suffixLink = self.root
        node.start = start
        node.end = end
        node.suffixIndex = -1
        return node

    def extend_suffix_tree(self, pos):
        global leafEnd
        leafEnd = pos
        self.remainingSuffixCount += 1
        self.lastNewNode = None
        while(self.remainingSuffixCount > 0):
            if (self.activeLength == 0):
                self.activeEdge = pos  
            if (self.activeNode.children.get(self._string[self.activeEdge]) is None):
                self.activeNode.children[self._string[self.activeEdge]] = self.new_node(pos, leaf=True)
                if (self.lastNewNode is not None):
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None
            else:
                _next = self.activeNode.children.get(self._string[self.activeEdge])
                if self.walk_down(_next):  
                   
                    continue
                if (self._string[_next.start + self.activeLength] == self._string[pos]):
    
                    if((self.lastNewNode is not None) and (self.activeNode != self.root)):
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    # APCFER3
                    self.activeLength += 1
                    break
                self.splitEnd = _next.start + self.activeLength - 1
                
                split = self.new_node(_next.start, self.splitEnd)
                self.activeNode.children[self._string[self.activeEdge]] = split
                
                split.children[self._string[pos]] = self.new_node(pos, leaf=True)
                _next.start += self.activeLength
                split.children[self._string[_next.start]] = _next
                
                if (self.lastNewNode is not None):
                    
                    self.lastNewNode.suffixLink = split
                
                self.lastNewNode = split
            
            self.remainingSuffixCount -= 1
            if ((self.activeNode == self.root) and (self.activeLength > 0)):  # APCFER2C1
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
            elif (self.activeNode != self.root):  # APCFER2C2
                self.activeNode = self.activeNode.suffixLink

    def walk_dfs(self, current):
        start, end = current.start, current.end
        yield self._string[start: end + 1]

        for node in current.children.values():
            if node:
                yield from self.walk_dfs(node)

    def build_suffix_tree(self):
        self.size = len(self._string)

        self.rootEnd = -1
        self.root = self.new_node(-1, self.rootEnd)
        self.activeNode = self.root  
        for i in range(self.size):
            self.extend_suffix_tree(i)

    def __str__(self):
        return "\n".join(map(str, self.edges.values()))

    def print_dfs(self):
        for sub in self.walk_dfs(self.root):
            print(sub)


