class Node:
    #Constructor Node() creates node
    def __init__(self,word):
        self.word = word
        self.right = None
        self.left = None
        self.count = 1

class BSTree:
    #Constructor BSTree() creates empty tree
    def __init__(self, root=None):
        self.root = root
        
    #Find word in tree
    def find(self, word):
        return _find(self.root, word)
    
    #Add node to tree with word
    def add(self, word):
        if not self.root:
            self.root = Node(word)
            return
        _add(self.root, word)

    #Print in order entire tree
    def in_order_print(self):
        _in_order_print(self.root)

    def size(self):
        return _size(self.root)

    def height(self):
        return _height(self.root)


#Function to add node with word as word attribute
def _add(root, word):
    if root.word == word:
        root.count +=1
        return
    if root.word > word:
        if root.left == None:
            root.left = Node(word)
        else:
            _add(root.left, word)
    else:
        if root.right == None:
            root.right = Node(word)
        else:
            _add(root.right, word)
    

def _find(root, word):
    """this functions recursively performs a binary search to see if the word is in the tree -
        if so, returns the number of times the word appears in the input text file"""
    if root.word == word:
        return root.count
    elif root.word > word:
        return _find(root.left, word)
    else:
        return _find(root.right, word)


def _size(root, size_tree=1):
    """this functions returns the number of nodes in the tree"""
    if root == None:
        size_tree = 0
        return size_tree
    if root.left != None:
        size_tree += 1
        size_tree = _size(root.left, size_tree)
    if root.right != None:
        size_tree += 1
        size_tree = _size(root.right, size_tree)
    return size_tree


def _height(root):
    """this functions returns the depth of the tree: a tree consisting only
    of one item (root) has a height of 1, an empty tree has a height of 0"""
    if root != None:
        left_depth = _height(root.left)
        right_depth = _height(root.right)
        if left_depth > right_depth:
            return left_depth + 1
        else:      
            return right_depth + 1
    else:
        return 0


#Function to print tree in order
def _in_order_print(root):
    if not root:                #if root == None       #if root is None
        return
    _in_order_print(root.left)
    print(root.word)
    print(root.count)
    _in_order_print(root.right)
