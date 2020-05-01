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
# str-ING FUNCTIONS

def flag(function, item):
    '''Returns the duple ( function(item), item ).
            >>> flag(lambda n: n == 42, 42)
            (True, 42)
    '''
    return function(item), item

def flag_all(function, iterable):
    '''Returns a map of flag-ged items.
            >>> flag(lambda n: n == 42, (42, 43))
    '''
    return map(partial(flag, function), iterable)

def strfindamong(string, iterable=WHITESPACES_ASCII):
    '''Similar to str.find, except that a search is conducted
    for any substrings of the iterable argument. Example:
    strfindamong('punctuation, such as the comma, may be included.', (',', '.'))'''
    index = min(chain((len(string),), filter(
        partial(argswap(greaterorequal), 0),
        map(string.find, iterable))))
    return -1 if index == len(string) else index


def strtail(string, delimiters=WHITESPACES_ASCII):
    '''Returns the "tail" of the string, where the tail begins
    with the first delimiter found in the string.'''
    i = strfindamong(string, delimiters)
    return '' if i < 0 else string[i:]




def csv(*string_iterables, sep=','): ###
    '''Returns a generator that, for each string-iterable in
    string_iterables, yield-s a corresponding line of text
    formed by joining the strings with sep and appending the
    newline character. Example:
            >>> printbare(*csv(
            ...     ('1', '2', '3', '4'),
            ...     ('1', '4', '9', ''),
            ...     (),
            ...     ('', '16')  ))
            1,2,3,4
            1,4,9,

            ,16
    '''
    return map(compose(line, partial(str.join, sep)), string_iterables)


def partitions(strings, seps=(NEWLINE,)):
    '''"Partition Ess." Repeatedly partition the strings found
    in the strings iterable using all of the seps. Example:
            >>> print(*partitions(
            ...     ('-pi:', '{0:e}'.format(-pi),),
            ...     (':', '.', 'e', 'E', '+', '-')))
            - 3 . 141593 e + 00
    '''
    for sep in seps:
        old = ()
        while strings != old:
            old = strings
            strings = tuple(chain(*mapchain(
                strings,
                partial(argswap(str.partition), sep),
                partial(tuplefilter, None) # remove null strings
            )))
    return strings

def charactermap(string):
    '''The purpose of this function is to define, by way of
    example, a charactermap: an iterator of strings of length 1.'''
    return iter(string)

def stream(strings, parse=towords):
    '''Returns a generator that yield-s substrings from the
    str-s produded by the strings iterable. atomic values from Originally intended to process text stored in lines of a
    text file (e.g., strings == iter(some_file)). yields one
    word at a time, where words are parsed one 'line' at a time
    according to the optional parse function (arg 1). Examples:
            >>> printbare(*iter(rewind(f))) # display file content:
              0  1  2
              3  4  5
              6  7  8
              9
            >>> print(*stream(iter(rewind(f)))) # every word
            0 1 2 3 4 5 6 7 8 9
            >>> print(*stream(skip(iter(rewind(f))))) # every word beyond first line
            3 4 5 6 7 8 9
            >>> print(*stream(quota(skip(iter(rewind(f)))))) # every word on the second line
            3 4 5
            >>> tuplemap(int, stream(rewind(f)))
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    '''
    for string in strings:
        for substring in parse(string):
            yield substring

def strenclose(s, left='"', right=None):
    character = {'(': ')', '[': ']', '{': '}', '<': '>'}
    if not right:
        right = left if left not in character else character[left]
    return left + s + right

def enquote(s=None, kind='double'):
    kinds = {'single': ("'",)*2, 'double': ('"',)*2,
        'tripple':("'''",)*2, 'back': ('`',)*2, 'singletypographic': ('`',
          "'"), 'doubletypographic': ('``', "''")}
    if not isinstance(s, str):
        return 'Choose kind in: ' + ' '.join(kinds.keys())
    if kind not in kinds:
        return s
    return strenclose(s, *kinds[kind])

def prefix(pre, s):
    return pre + s

def strlstrip(s, chars=''):
    return s.lstrip(chars)

def strreplace(s, old='', new='', count=-1):
    if count < 0:
        return s.replace(old, new)
    return s.replace(old, new, count)

def strfirst(s): ###
    if len(s):
        return s[0]
    return ''

def strfirstn(s, n=1): ###
    'Returns a string containing the first n characters of s.'
    if n < 1:
        return ''
    if len(s) < n:
        return s
    return s[:n]

def strlastn(s, n=1): ###
    'Returns a string containing the last n characters of s.'
    if n < 1:
        return ''
    if len(s) < n:
        return s
    return s[-n:]

def strsplitn(s, n=1):
    '''Returns a duple containing 0) a string containing the
    first n characters of s and 1) a string containing the
    remaining characters of s.'''
    return strfirstn(s, n), strlastn(s, len(s) - n)

def anagrams(s, iterable):
    '''Primary argument is a string. Secondary argument is an
    iterable of iterables. The inner iterables produce integers
    which are indices into s. Returns a map of strings, where
    each string is formed from the characters of s specified by
    the inner iterables. Produces true anagrams if and only if
    the inner iterables specify each character of s only once.
        Examples:
    >>> print(*anagrams('a', (range(1),)))
    a
    >>> print(*anagrams('AMANAPLANACANALPANAMA', 
    ... ranges(((1,), (1,4), (4,5), (5,9), (9,10), (10,15), (15,21)))))
    A MAN A PLAN A CANAL PANAMA
    >>> print(*anagrams('AMANAPLANACANALPANAMA', 
    ... ranges(((0,-1,-1), (-2,-5,-1), (-5,-6,-1), (-6,-10,-1), (-10,-11,-1), (-11,-16,-1), (-16,-22,-1)))))
    A MAN A PLAN A CANAL PANAMA
    '''
    from functools import partial
    pmembers = partial(members, s)
    return map(strcat, membersets(s, iterable))

def strsplitfixedwidth(s, iterable):
    '''Returns consecutive substrings of s according to the
    iterable, which produces a sequence of starting columns for
    each substring; the last value produced from the iterator
    should be one more than the last column desired, and may be
    equal to the length s.
        TO DO: refactor using chunks function.
    >>> #    0         1         2
    >>> #    0123456789012345678901
    >>> s = 'AMANAPLANACANALPANAMA'
    >>> print(tuple(strsplitfixedwidth(s,
    ... (0, 1, 4, 5, 9, 10, 15, len(s)))))
    ('A', 'MAN', 'A', 'PLAN', 'A', 'CANAL', 'PANAMA')
    '''
    return anagrams(s, partition(iterable))

def strsplitfixedwidthuniform(string, length=1):
    '''Returns a map of substrings of string, each of the given
    length, except possibly the final substring, which will be of
    a shorter length if len(string) is not a multiple of length.
    Concatenating the substrings produced will recover the
    original string.  Example:
            >>> tuple(strsplitfixedwidthuniform(
            ... 'SATORAREPOTENETOPERAROTAS\n', 5))
            ('SATOR', 'AREPO', 'TENET', 'OPERA', 'ROTAS', '\n')
    '''
    assert isinstance(string, str), 'primary argument must be str.'
    assert isinstance(width,  int), 'secondary argument must be int.'
    assert 0 < width, 'width must be positive.'
    return map(strcat, chunks(iter(string), steady(width)))

def strstrip(s): ###
    return s.strip()

def strupper(s): ###
    return s.upper()

def strsplit(s, sep=None): ###
    return tuple(s.split(sep))

def strsplittab(s): ###
    return tuple(s.split('\t'))

def compoundstring():
    '''A compund string is a string that represents more than on
    e string. A compound string begins with a separator
    character by which it may be split into the constituent
    strings. The constituent strings may themselves be compound
    strings.'''
    assert False, '''this function serves only to document
    "compound string"'''

def strsplit0(string): ###
    '''split-s the tail of string using the initial member of
    string as a separator. Returns the result of the split.
    However, if there is noting to split, returns (). History:
    2017-12-28: changed exception return to []. 2018-03-30:
    changed to return tuples.'''
    if len(string) < 2:
        return ()
    return tuple(string[1:].split(string[0]))

def strfirstword(s, sep=None): ###
    'Returns the first word of string s'
    t = s.split(sep=sep, maxsplit=1)
    if not len(t):
        return ''
    return t[0]

def strnoeolcomments(st, c='#'): ###
    return st.split(c, 1)[0].strip()

def join(*strings): ### #TAGS: concatenate
    return ''.join(strings)

def strpad(string, n, characters=SPACE):
    '''In the trivial case, returns string if n <= len(string).
    Otherwise, returns a string of length n whose left elements are taken
    from characters. Characters are recycled if needed to obtain
    the quantity required. Examples:
            >>> strpad(hex(15)[2:], 4, '0')
            '000f'
            >>> strpad("1", 39, ". ")
            '. . . . . . . . . . . . . . . . . . . 1'
    '''
    return join(*pad(string, n, characters))[-max(len(string), n):]

def strcat(sequence, sep=''): ### tag: concatenate strings join
    return sep.join(sequence)

def PLACEHOLDER(): # def strcats # tags: concatenate words sentences strings
    pass
strcats = partial(strcat, sep=' ')

def wordsasline(words):
    return strasline(joinwords(words))

def unparse(*strings, sep=' '):
    '''Each of the strings arguments is intended to be a
    "column" (e.g., a
    tuple or map) of strings. Returns a map of the corresponding
    "rows". Example: the function call
            print(*unparse(('Deg C', '-42', '0', '100'), 
                    ('Deg F', '-42', '32', '212'), sep=','),
                    sep='\n.')
    print-s the following to stdout:
    Deg C,Deg F
    -42,-42
    0,32
    100,212
    Note the subtle difference between these two calls:
    >>> print(*unparse('abc','def')) # unparse arguments are two strings
    a d b e c f
    >>> print(*unparse(('abc','def'))) # unparse argument is tuple of two strings
    abc def
    '''
    from functools import partial
    return map(sep.join, zip(*strings))

