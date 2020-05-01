# Text Processor
# Copyright (C) 2019 D. Michael Parrish
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



def issingleline(string):
    '''returns a bool indicating whether the last character of
    the string is a newline character AND this is the only
    newline character.
    '''
    if not isline(string):
        return False
    if 1 != len(tuplefilter(partial(equal, '\n'), string)):
        return False
    return True

def isblankline(string, whitespace=whitespaces()):
    '''returns a bool indicating about the string argument
    whether there is only one newline character AND that the
    newline character occurs at the end AND that there string
    contains only whitespace (where whitespace is given by the
    whitespace argument).
    '''
    if not issingleline(string):
        return False
    for c in filter(un(partial(fnin, whitespace)), string):
        return False
    return True

def cleanblanklines(strings):
    '''yield-s a string corresponding to each item of the
    strings iterable argument. Each yield-ed string is either
    the same as the corresponding item if it is not a blank
    line or a "clean blank line" (i.e., "\n") if it is a blank
    line.
    '''
    for string in strings:
        yield string if not isblankline(string) else '\n'

def unindent(string_iterable):
    '''Returns as lines of text the strings of the
    string_iterable argument, with the initial whitespace
    stripped.
    '''
    return map(compose(line, str.lstrip), string_iterable)

def unfmt(string): #TAGS format paragraph unindent
    '''unfmt (unformat) returns a tuple of strings formed by
    removing leading whitespace from each of the lines of the
    string and removing leading and trailing blank lines.

    Originally developed for the purpose of including multiline
    strings in source code that also follow an indentation
    style similar to Python 3 (but simpler, as no indentation
    remains in the return).

    >>> unfmt("""
        This is a
        multiline
        string
        """)
    ('This is a\n', 'multiline\n', 'string\n')
    '''
    return lrfilter(unindent(strsplit_(string)), un(partial(equal, '\n')))

def strremove(string, old, *count):
    '''same as str.replace, EXCEPT that new is fixed at the null
    character.
    '''
    return string.replace(old, NULL, *count)

strremovecommas = partial(argswap(strremove), COMMA)
