# AnPaFinder
Version 1.2.2 released 04/2022

A simple package built to find anagrams and palindromes from a webpage. 
Includes functionality to store and process strings and substrings, 
and easily parse text from a webpage.

## Installation
`AnPaFinder` can be installed via `pip`:
```
$ python3 -m pip install AnPaFinder
```

-Find the anagrams and palindromes from a webpage in one of three possible ways:
 - Option 1. In python environment:
   ```
   import anpa_tools.anpatools as anp
   anp.find_anpas("<webpage url>")
   ```
 - Option 2. Run anpatools.py from command line:
   ```
   $ python3 anpatools.py --url "<webpage url>"
   ```
 - Option 3. Using the shell script in the **Home Page - anpaFinder GitHub repository** under `/bin`:
   ```
   $ ./AP_finder.bash -w "<webpage url>"
   ```
-Play with classes and functions in `anpa_tools` package.
 - More info to come
		