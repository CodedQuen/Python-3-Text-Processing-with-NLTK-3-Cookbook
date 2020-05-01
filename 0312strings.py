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



def chrs(character_code_iterable):
    '''Returns a map that produces the characters whose
    character codes are produced by the argument.'''
    return map(chr, character_code_iterable)

def whitespaces(character_code_iterable=range(128)):
    '''Returns a frozenset of whitespace characters whose
    character codes are produced by the argument (defaults to
    ASCII range). Whitespace is defind by str.strip.
    '''
    return frozenset(filter(
        un(str.strip), chrs(character_code_iterable)))
    # * GUARANTEED: len(c) == 1

WHITESPACES_ASCII = whitespaces()

def strfindall(string, sub):
    '''generates all indices in string where substring sub is
    found, in the oder that they are found. Cf. str.find.
    '''
    start = 0
    while start < len(string):
        start = string.find(sub, start)
        if start < 0:
            break
        yield start
        start += 1


NULL = ''

def isline(string):
    '''Returns a bool that tells whether the argument is a
    string whose last character is the newline character.'''
    if (not string) or (not isinstance(string, str)):
        return False
    return string[-1] == NEWLINE

def line(string):
    '''Returns the string argument if it already ends in
    new-line. Otherwise returns a modified copy of the string
    argument which consists of the concatenation of the string
    argument and newline.'''
    return string + ('' if isline(string) else NEWLINE)

