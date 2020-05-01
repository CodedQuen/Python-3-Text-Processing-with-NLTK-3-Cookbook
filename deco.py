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
# See also clu.py for additional examples

def fnstrstofnstr(function):
    '''The function argument is a funciton of zero or more
    strings.  decoA returns a funciton that is a function of a
    single, compound string. Example (code for decoAexample0
    elsewhere):
    .
            >>> decoAexample0(' threescore years and ten')
            threescore-years-and-ten
    '''
    def inner(st):
        printerr('(STATUS) fnstrstofnstr (inner): strsplit0(st):', *strsplit0(st), sep='\n    -->',
                end='\n\n')
        return function(*strsplit0(st))
    return inner

@fnstrstofnstr
def fnstrstofnstrExample(a, b, c, d):
    print(a, b, c, d, sep='-')

def fnargkwargtofnstrs(function):
    '''The function argument is a function of either 0) no
    arguments, 1) one or more positional arguments, 2) one or
    more keyword arguments, 3) both positional and keyword
    arguments. All of the arguments mentiond in the foregoing
    list are strings. Returns a function of zero or more
    strings, the first of which (if present) represents the
    positional argumens, and the second of which (if present)
    represents  the keyword arguments mentioned in the previous
    sentence.'''
    def inner(*st):
        printerr('(STATUS) fnargkwargtofnstrs (inner): *st',
                *st, sep='\n    ==> ')
        if not st:
            return function()
        st0 = strsplit0(st[0])
        printerr('(STATUS) fnargkwargtofnstrs (inner): st0',
                *st0, sep='\n    ==> ')
        if len(st) < 2:
            return function(*st0)
        printerr('(STATUS) fnargkwargtofnstrs (inner): using dictionary form.')
        printerr('(STATUS) fnargkwargtofnstrs (inner): st0:', st0)
        printerr('(STATUS) fnargkwargtofnstrs (inner): dictfromstr(st[1]):', dictfromstr(st[1]))
        printerr('(STATUS) function:', function)
        return function(*st0, **dictfromstr(st[1]))
    return inner

@fnstrstofnstr
@fnargkwargtofnstrs
def decoBexample0():
    print(None)

@fnstrstofnstr
@fnargkwargtofnstrs
def decoBexample1(s0, *s):
    print(s0)
    print(*s, sep=', ')

@fnstrstofnstr
@fnargkwargtofnstrs
def decoBexample2(kw0=7, **kw):
    print(kw0)
    print(kw)

def fnfndargkwatofnstrstr(function):
    '''Given a function of a filename dictionary, other
    arguments and keyword arguments, returns a function of a
    compound string.'''
    def inner(strstr):
        printerr('fnfndargkwatofnstrstr inner: strstr:', strstr)
        fnd, arg, kwa = strstr_to_fnd_arg_kwa(strstr)
        printerr('fnfndargkwatofnstrstr inner: fnd:', fnd)
        printerr('fnfndargkwatofnstrstr inner: fnd:', arg)
        printerr('fnfndargkwatofnstrstr inner: fnd:', kwa)
        return function(fnd, *arg, **kwa)
    return inner

@fnfndargkwatofnstrstr
def fnfndargkwatofnstrstrExampleA(filename_dictionary, a0, a1 ,a2, *aa, kw0='keyword0', kw1='keyword1'):
    print(filename_dictionary)
    print(a0, a1, a2, *aa)
    print(kw0, kw1, **kw)

@fnfndargkwatofnstrstr
@decoopend
def utilityExample(files): #, a): #, a, b, *c, kw0=0, kw1=1):
    print(files['r'][0].read())
    #print(a)

