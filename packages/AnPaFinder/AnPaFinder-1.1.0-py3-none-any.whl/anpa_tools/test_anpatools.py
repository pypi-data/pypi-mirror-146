# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 15:45:33 2022

@author: aarid

Tests for anpatools
"""

import unittest
import os

import anpatools

testlist = ['dog', 'god', 'onyx', 'silent', 'listen']

class StringObjectTests(unittest.TestCase):
    """Test for correct output for each method in class"""
    def setUp(self):
        """Instantiate class object and set variables"""
        self.string_a = anpatools.StringObject('listen')
        self.substring = self.string_a.substring(' silent')

    def test_append(self):
        """Call function, test fails if output not equal to expected."""
        appended_string = self.string_a.append()
        self.assertEqual(appended_string, 'listen silent')

    def test_remove(self):
        """Call function, test fails if output not equal to expected."""
        truncated_string = self.string_a.remove()
        self.assertEqual(truncated_string, 'listen')

    def test_mirror_string(self):
        """Call function, test fails if output not equal to expected."""
        mirror = self.string_a.mirror_string()
        self.assertEqual(mirror, 'netsil')

    def test_load_string(self):
        """Call function, test fails if output not equal to expected."""
        loaded_string = self.string_a.load_string('test_loadfile.txt')
        self.assertEqual(loaded_string, 'data loaded')

    def test_save_string(self):
        """Call function, test fails if output not equal to expected."""
        expected = self.string_a.string
        save_file = 'test_savefile.txt'
        try:
            self.string_a.save_string(save_file)
            with open(save_file, 'r') as s_f:
                text = s_f.read()
        finally:
            os.remove(save_file)
        self.assertEqual(expected, text)

class AnagramTests(unittest.TestCase):
    """Test for correct output for each method in class"""
    def setUp(self):
        """Instantiate class object and set variables"""
        self.ana = anpatools.Anagram()

    def test_find_anagrams(self):
        """Call function, test fails if output not equal to expected."""
        anagram_groups = self.ana.find_anagrams(testlist)
        expected = [['dog', 'god'], ['silent', 'listen']]
        self.assertEqual(anagram_groups, expected)

    def test_create_all_anagrams(self):
        """Call function, test fails if output not equal to expected."""
        pass

class PalyndromTest(unittest.TestCase):
    """Test for correct output for each method in class"""
    def setUp(self):
        """Instantiate class object and set variables"""
        self.pal = anpatools.Palyndrome('hannah')

    def test_find_palindromes(self):
        """Call function, test fails if output not equal to expected."""
        mirror = self.pal.find_palindromes()
        self.assertEqual(mirror, 'hannah')


unittest.main()
