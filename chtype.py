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
################################## chtype.py ##################################
# cf. ctype.h in C
# HISTORY
#       2018-04-25: redesigned isprint, isgraph; created
#       isasciicode, isasciicodecontrol. removed isch

def isstr(obj): ###
    return isinstance(obj, str)

def ischaracter(obj): #.#
    return isstr(obj) and len(obj) == 1

def incharacterrange(obj, character_range=(chr(32), chr(127))):
    '''Returns a bool indicating whether the primary argument is
    a character in the range of characters given. Return False
    for all noncharacter arguments.'''
    return (
        ischaracter(obj) and
        ord(first(character_range)) <= ord(obj) and
        ord(obj) <= second(character_range))

isdigit = partial(incharacterrange, character_range=('0', '9'))
islower = partial(incharacterrange, character_range=('a', 'z'))
isupper = partial(incharacterrange, character_range=('A', 'Z'))
isletter = lambda obj: islower(obj) or isupper(obj)

isasciicode = lambda n: isint(n) and 0 <=n and n < 128

def isasciichar(c):
    return isasciicode(ord(c))

def isasciicodecontrol(n):
    return (n < 32) or (n == 127)

def isprint(character):
    'V.s. Python isprintable method; C.f. isprint function in C.'
    try:
        code = ord(character)
    except:
        return False
    return isasciicode(code) and not isasciicodecontrol(code)

def isgraph(character):
    '''cf. the isgraph funciton from the C programming language.
    Tests only the first item in the string argument. Characters
    tested are assumed to be in the ASCII set, UTF-8 code page
    U+0000, or equivalent.'''
    return isprint(character) and (character != ' ')

def asciicharacters():
    '''Returns a map of ASCII characters. HISTORY: 2018-10-05
    formerly returned a tuple.'''
    return map(chr, range(128))

def asciicharactersprint():
    '''Returns a map of printing ASCII characters. HISTORY:
    2018-10-05 formerly returned a tuple.'''
    return filter(isprint, asciicharacters())

def maskchars(string, keep=isasciichar, replacement=SPACE):
    '''Returns a str like string, except that characters for
    which keep returns false are replaced with replacement.'''
    return strcat([c for c in map(lambda h: h if keep(h) else replacement, string)])

'''
def isch(): #REMOVED
'''
