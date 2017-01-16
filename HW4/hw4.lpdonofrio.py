# Prompt: perform a search engine function based on input from the user on the given

import urllib.request as re;
import urllib.error as er;
import string

def read_catalog(catalog_file):
    """reads catalog file and creates the dictionary 'books' and the lists 'titles' and 'links'"""
    with open(catalog_file, 'r') as catalog:
        lines = catalog.read().splitlines()
    books_list = []
    for item in lines:
        inner_list = []
        if item.find(',http') != -1:
            comma_valid = item.find(',http')
            inner_list.append(item[0:comma_valid])
            inner_list.append(item[comma_valid+1:])
            books_list.append(inner_list)
        else:
            print("The entry '{}' does not follow the input convention".format(item))
            continue
    books = {}
    titles = []
    links = []
    for item in books_list:
        order = books_list.index(item)
        if item[0] not in books:
            books[item[0]] = [order, item[1]]
            links.append(item[1])
            titles.append(item[0])
        else:
            continue
    return books, titles, links


def read_book(url):
    """for each book in books, reads the url, converts upper-case letters to lower-case letters,
       discards punctuation, handles exceptions"""
    try:
        response = re.urlopen(url)  # open url
        content = response.read()   # get data
        response.close()            # close connection
        content_string = content.decode('utf-8')
        filter_punc = lambda t: ''.join([x.lower() for x in t if x.isalpha()])
        words = [x for x in map(filter_punc, content_string.split()) if x]
        return words
    except(er.URLError):
        content = ""
        print("The url is not functional: " + url)
    except:
        print("This is not an url: " + url)

def create_dict(books, titles):
    words_dict = {}
    for key, value in books.items():
        title_index = value[0]                              #gives me position of the book in the original text file
        words_list = read_book(value[1])                    #gives me list of words in the book (cleaned)
        try:
            for word in words_list:
                if word not in words_dict:                      #if the word is not in the dictionary
                    words_dict[word] = [0]*len(titles)          #create list of 0's whose length corresponds to the number of books
                    words_dict[word][title_index] += 1          #adds 1 in the list's location corresponding to the title index
                else:                                           #if the word is not in the dictionary
                    words_dict[word][title_index] += 1          #adds 1 in the list's location corresponding to the title index
        except:
            continue
    return words_dict

def search_dict(words, titles_list, books, links):
    """prints the count, handles terminate, catalog, etc."""
    while True:
        lookup_word = input("Search term? ")
        if lookup_word == "<terminate>":
            return
        elif lookup_word == "<catalog>":
            for title in titles_list:
                print("'{}' : [{}, '{}']".format(title, titles_list.index(title), links[titles_list.index(title)]))
        elif lookup_word == "<titles>":
            for title in titles_list:
                print(title)
        elif lookup_word in words:
            books_counts = words[lookup_word]
            books_counts_index = [(books_counts[i],titles_list[i],links[i]) for i in range(len(books_counts))]
            books_counts_index.sort(reverse=True)
            count = 1
            for c in books_counts_index:
                if c[0] == 0:
                    continue
                elif c[0] == 1:
                    print("{}. The word {} appears {} time in {} (link: {})".format(count, lookup_word, c[0], c[1], c[2]))
                else:
                    print("{}. The word {} appears {} times in {} (link: {})".format(count, lookup_word, c[0], c[1], c[2]))
                count += 1
        else:
            print("The word {} does not appear in any books in the library".format(lookup_word))


#########################################################################

def main():

    try:
        books, titles, links = read_catalog('catalog.txt')
    except:
        print("The file 'catalog.txt' was not found. Sorry!")
        return
    if books == {} or titles == []:
        print("No books to search. Sorry!")
        return
    words_dict = create_dict(books, titles)
    search_dict(words_dict, titles, books, links)

if __name__ == "__main__":
    main()


