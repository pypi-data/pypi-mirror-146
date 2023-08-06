# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 05:48:02 2022

@author: aarid
"""

import itertools
from collections import Counter, defaultdict
from html.parser import HTMLParser
import urllib.request
import string as strimp
import argparse


class StringObject:
    """Various functions for stored strings"""
    def __init__(self, string):
        self.string = string
        self.sub_string = None
        self.loaded_string = None
        self.save_file = None


    def __repr__(self):
        """Return a string representation of string object"""
        return self.string

    def substring(self, substring):
        """set value of self.sub_string"""
        self.sub_string = substring
        return self.sub_string

    def append(self):
        """
        Appends a sub_string to string, and returns the appended string.

        >>> test = StringObject()
        >>> test.string = 'This is my string'
        >>> print(test.string)
        This is my string
        >>> test.sub_string = ', but only for now.'
        >>> print(test.append(test.sub_string))
        This is my string, but only for now.
        """
        appended = str(self.string) + str(self.sub_string)
        return appended

    def remove(self):
        """
        Removes a sub_string from string, and returns the truncated string.

        >>> test = StringObject()
        >>> test.string = 'This is my string, but only for now.'
        >>> print(test.string)
        This is my string, but only for now.
        >>> test.sub_string = ', but only for now.'
        >>> print(test.remove(test.sub_string))
        This is my string
        >>> test.sub_string = 'This is my string,'
        >>> print(test.remove(test.sub_string))
        but only for now.
        """
        truncated = self.string.replace(str(self.sub_string), '')
        return truncated

    def mirror_string(self):
        """
        Returns the mirrored string of string.

        >>> test = StringObject()
        >>> test.string = 'This is my string'
        >>> print(test.string)
        This is my string
        >>> print(test.mirror_string())
        gnirts ym si sihT
        """
        mirror = str(self.string[::-1])
        return mirror

    def load_string(self, load_file):
        """Loads a string from load_file and returns that string."""
        with open(load_file) as load_string:
            self.loaded_string = load_string.read()
        return self.loaded_string

    def save_string(self, save_file):
        """Saves the string to save_file."""
        with open(save_file, 'w') as saved:
            saved.write(self.string)


class Anagram(StringObject):
    """Inherits from StringObject class and can get anagrams of string."""
    def __init__(self):
        super().__init__(self)
        self.string = None
        self.words = []

    def find_anagrams(self, words):
        """Takes a list of words, and hashes the letter frequency of each word
        as keys in a dictionary and creates a value list to which words having
        the same letter frequency are appended to the list. Returns the values
        if the length of the list is greater than 1.
        """
        anagrams_dict = defaultdict(list)
        self.words = words
        for word in words:
            if len(word) > 2:
                anagrams_dict[frozenset(dict(Counter(word)).items())].append(word)
        return [anagrams for key, anagrams in anagrams_dict.items() if len(anagrams) > 1]


    def create_all_anagrams(self):
        """Takes string and returns a list of string's anagrams (permutations)."""
        anagrams = [''.join(perm) for perm in itertools.permutations(self.string)]
        return anagrams


class Palyndrome(StringObject):
    """Inherits from StringObject and can identify palindromes."""
    def __init__(self, string):
        super().__init__(self)
        self.string = string

    def find_palindromes(self):
        """Checks if mirrored string is equal to string.
        If true, returns the mirrored string."""
        mirror = StringObject.mirror_string(self)
        if mirror == str(self.string) and len(mirror) > 2:
            palindrome = mirror
            return palindrome


class ParserHTML(HTMLParser):
    """Inherits from HTMLParser in python standard library.
    Parses text from inside <p> tags, adds text to a list, returns the list"""
    data_list = []
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_data = False
    def handle_starttag(self, tag, attrs): #why the attrs parameter?
        if tag == 'p':
            self.is_data = True
    def handle_endtag(self, tag):
        if tag == 'p':
            self.is_data = False
    def handle_data(self, data):
        if self.is_data:
            self.data_list.append(data)
        return self.data_list
 
    
def access_webpage(url):
    """
    Opens and reads a webpage from URL and returns raw HTML from webpage.
    """
    webpage = urllib.request.urlopen(url)
    content = webpage.read().decode()
    return content

def parse_page(content):
    """
    Takes raw html as input and parses text from <p> tags.
    Returns a list of parsed text
    """
    pars = ParserHTML()
    pars.feed(str(content))
    parsed_data = pars.data_list
    return parsed_data

def clean_data(data_list):
    """
    Takes a list of strings and iterates through the list to make all letters 
    lowercase and remove punctuation. Appends the cleaned strings to a new 
    list. Returns the new list.
    """
    string_list = []
    for item in data_list:
        item = item.lower()
        item = item.translate(str.maketrans('', '', strimp.punctuation))
        string_list.append(item)
    return string_list

def split_sentence(string_list):
    """
    Takes a list of sentences or multi-word strings and iterates through the 
    list to split each sentence into a list of words. Iterates through the 
    words, and appends each word once to a new list. Returns new list.
    """
    word_list = []
    for items in string_list:
        words = items.split(' ')
        for word in words:
            word = word.replace('\n', '')
            word = word.replace('\\', '')
            if word != '' and word not in word_list:
                word_list.append(word)
    return word_list

def find_anpas(URLin):
    """Takes a web address (string) as input and returns a list of anagram
    sets and palindromes from the web page."""
    web_content = access_webpage(URLin)
    parsed_list = parse_page(web_content)
    data_strings = clean_data(parsed_list)
    data_words = split_sentence(data_strings)
    print("\n\nAnagrams:")
    anagrams = Anagram()
    anagram_groups = anagrams.find_anagrams(data_words)
    print(anagram_groups)

    print("\n\nPalindromes:")
    palindromes = [Palyndrome(n) for n in data_words]
    for palyndrome in palindromes:
        pal = palyndrome.find_palindromes()
        if pal is not None:
            print(pal)


if __name__ == '__main__':
    #Add command line argument
    parser = argparse.ArgumentParser(description='Process web url.')
    parser.add_argument('--url', type=str, required=True,\
                    help='Web address to the page to analyze.')


    #Assign command line arguments
    args = parser.parse_args()
    URL = args.url

    #Function calls
    web_content = access_webpage(URL)
    parsed_list = parse_page(web_content)
    data_strings = clean_data(parsed_list)
    data_words = split_sentence(data_strings)

    print("\n\nAnagrams:")
    anagrams = Anagram()
    anagram_groups = anagrams.find_anagrams(data_words)
    print(anagram_groups)

    print("\n\nPalindromes:")
    palindromes = [Palyndrome(n) for n in data_words]
    for palyndrome in palindromes:
        pal = palyndrome.find_palindromes()
        if pal is not None:
            print(pal)
