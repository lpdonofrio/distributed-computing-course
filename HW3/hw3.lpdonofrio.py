# Prompt: implement a word-count program using a binary search tree

from BST import *

def read_file(filename):
    with open(filename, 'rU') as document:
        text = document.read()
    filter_punc = lambda t: ''.join([x.lower() for x in t if x.isalpha()])
    words = [x for x in map(filter_punc, text.split()) if x]
    return words


def main():
    while(True):
        print("Enter the file name to read:")
        filename = input('> ')
        try:
            words = read_file(filename)
        except IOError:
            print("Unable to find the file {}".format(filename))
        else:
            tree = BSTree()
            for word in words:
                tree.add(word)
            lookup_word = ""
            while(True):
                lookup_word = input('Query:  ')
                size_tree = tree.size()
                depth_tree = tree.height()
                if all(letter.islower() for letter in lookup_word):
                    if lookup_word == "stats":
                        print("The number of entries in the tree is {} and the maximum "
                                "depth of the tree is {}".format(size_tree, depth_tree))
                        continue
                    if lookup_word == "terminate":
                        return
                    try:
                        times = tree.find(lookup_word)
                        print("The word {} appears {} times in the tree".format(lookup_word, times))
                    except:
                        print("The word {} is not in the tree".format(lookup_word))
                else:
                    print("Please input only lower case alphabetic characters and do not include spaces")
                    continue

if __name__ == "__main__":
    main()