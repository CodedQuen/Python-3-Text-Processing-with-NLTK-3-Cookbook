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
NAMECHARS = set(chain(('`'), map(
    chr,
    chain(
        range(ord('0'), 1 + ord('9')),
        range(ord('A'), 1 + ord('Z')),
        range(ord('a'), 1 + ord('z'))))))

NAMECHARSALL = NAMECHARS.union(set('.'))

def exposed(lines, leadchars=NAMECHARS):
    return filter(lambda s: first(s) in leadchars, linesnonblank(lines))

def asnest(sequence):
    tpl = ()
    for item in reversed(sequence):
        lst = list(tpl)
        lst.insert(0, item)
        tpl = astuple(tuple(lst))
    return first(tpl)

def isRname(string):
    '''Returns a bool indicating whether the str argument is a
    valid R name or identifier'''
    if not len(string):
        return False
    return string[0].isalpha() or string[0] in tuple('.`')

def isRdef(line):
    '''Returns a bool indicating whether the line contains the
    beginning of an R function definition recognized by the
    pattern <BEGINNING OF LINE><R NAME><WHITESPACE><= OR <->
    <WHITESPACE>"function"
    '''
    words = towords(line)
    if len(words) < 3:
        return False
    return (words[2] == 'function') and (
            words[1] in ('=', '<-')) and (
            isRname(words[0]))

def RfuncDefSplit(line):
    '''Given a line containing a function definition, returns a
    tuple containing the function name and any tags.'''
    parts = line.strip().split()
    if (len(parts) < 4) or (parts[3] != '#'):
        return parts[0], ()
    return parts[0], tuple(parts[4:])

def Rfuncs(lines):
    return map(
        lambda x: tuple(flat(first(x), RfuncDefSplit(second(x)))),
        filter(
            lambda x: isRdef(second(x)),
            enumerate1(lines)))

def inlines(f=None):
    if not f:
        from sys import stdin
        f = stdin
    for line in lineiter(f):
        yield line

def everyRfunctionFromFileList(f=None):
    '''Sample Usage:
    dir *.R /b|u:\pygo "p:/R.py" Rfunctions ""
    '''
    if not f:
        from sys import stdin
        f = stdin
    filenames = f.read().split('\n')
    funcs = set()
    for filename in filter(None, filenames):
        with open(filename) as fi:
            funcs.update(set(
                map(lambda x: (filename,) + x,
                    Rfuncs(fi.readlines()))))
    return map(
        lambda x: dictzip(towords(
                'filename lineNo functionName themes'), x),
        funcs)

def everyRfunction(dummy_string):
    for item in everyRfunctionFromFileList():
        print(item)

def everyRtheme(dummy_string):
    themes = set()
    for item in everyRfunctionFromFileList():
        themes.update(item['themes'])
    lthemes = list(themes);   lthemes.sort()
    print(*lthemes)

def test(dummy_string, excluded=('function'), sort=True, ls_all=False):
    fltr = None
    if ls_all:
        fltr = lambda s: s[0] != '.'
    l = []
    for f in fileiter(map(linebare, linesnonblank(inlines()))):
        for line in filter(fltr, exposed(f)):
            words = towords(line)
            if words[0] not in excluded and 'function' in words:
                l.append(words[0])
    if sort:
        l.sort()
    print(*l, sep=eol())
