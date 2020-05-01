# Text Processor
# Copyright (C) 2018 D. Michael Parrish
# 
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#
# END OF COPYRIGHT NOTICE
#
#
# CONVERSIONS OF INDIVIDUAL WORDS

def NaN(): ### 2018-01-26: converted to funcdef (was value previously)
    return float('nan')

def nicefloat(string=''):
    '''Returns a float which has been converted from the string
    argument. Could return -inf or inf.'''
    try:
        return float(string)
    except:
        return NaN()

def niceint(string, default=NaN()):
    '''If possible, returns an int which has been converted from
    the string argument. Otherwise returns default (of type float).
    KNOWN ISSUE: some strings representing large-magnitude
    integers will be converted to -inf or inf, or to
    appriximate values. e.g., niceint('1e22') ==
    10000000000000000000000, but niceint('1e22') ==
    99999999999999991611392.'''
    try:
        return int(string)
    except:
        f = nicefloat(string)
        from math import isinf, isnan
        if isinf(f) or isnan(f):
            return default
        return int(f)

# CONVERSION OF STRINGS TO WORD-BASED ITEMS

def substrings(s=''):
    'Returns a list of words (substrings) found in the string argument.'
    return s.strip().split()

def ints(s=''):
    'Returns a list of int-s represented as substrings of the string argument'
    return list(map(niceint, substrings(s)))

def floats(s=''):
    'Returns a list of float-s represented as substrings of the string argument'
    return list(map(nicefloat, substrings(s)))

def intorfloat(iterable, function=None): ###
    '''The iterable produces duples where the first item is an
    int and the second is a float, and both values represent the
    same quantity, possibly with diferent precision. Applies
    function choose which of the two representations to emit. If
    function is not specified, int-s will be emitted, provided
    that the two values compare as equal.  Allusion: _The Lady
    or the Tiger?_'''
    def default(tpl):
        i, f = tpl
        if i == f:
            return i
        return f
    if function is None:
        function = default
    return map(function, iterable)

def nicenums(s=''): #.# 2018-01-26: corrections
    '''Returns a list of numeric values (each an int or a float) represeted as
    substrings of the string argument'''
    return tuple(intorfloat(zip(ints(s), floats(s))))

def lengths(s=''):
    'returns the lengths of each word in the string argument'
    return list(map(len, substrings(s)))


# CONVERSION OF WORD LISTS TO OTHER WORD LISTS

def sansnan(lst=[1,2.0,3]):
    return list(filter(lambda x: str(x) != 'nan', lst))


def linc(lst=[1,2.7,3.1]):
    '''Return a new list that is eqivalent to the argument (simple list of
    scalar numeric values) where each value has been incremented by one.'''
    
    return list(map(lambda x: 1 + x, lst))


# REDUCTION OF STRINGS, INTERPRETED AS WORDS, TO SINGLE ITEMS

def nicemax(s=''):
    '''Returns a string representing the maximum of the values represeted in the
    string argument. Returns the null string if maximum is undefined.'''
    n = nicenums(s)
    if len(n):
        return repr(max(n))
    return ''

def wordcount(s=''):
    return len(substrings(s))

def lengthoflongestword(s=''):
    lgt=lengths(s); return max(lgt) if len(lgt) else 0

def wordn(s='', n=0):
    if (wordcount(s) - 1) < n:
        return ''
    return substrings(s)[n]

def towordsn(s, n=1):
    '''Specialization of str.split. Returns a tuple containing
    the first n words found in the string argument s, followed
    by the substring found after those words. Whitespace before
    and between the first n words is discarded, as is whitespace
    found between the n-th word and any non whitespace
    characters that follow.'''
    assert isinstance(s, str), 'First argument must be str.'
    assert isinstance(n, int), 'Second argument must be int.'
    return tuple(s.split(None, n))

#REMOVED use product in arith.py
#def product(s=''):
    #from functools import reduce
    #return reduce(lambda x, y: x * y, sansnan(nicenums(s)), 1)
