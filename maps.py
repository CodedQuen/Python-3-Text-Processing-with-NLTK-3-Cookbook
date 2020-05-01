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
# map FUNCTIONS

def map0(function, iterable): ###
    '''A wrapper for map for functions of no variables. As with
    map, the number of values produced is consistent with the
    number produced by iterable.'''
    return map(lambda x: function(), iterable)

def mapmap(*iterables, function=str): ### #TAGS compound
    '''Returns a map that produces maps that produce the
    result of applying the function to items produced by each
    iterable of iterables. Originally intended to form a table
    of strings.
            >>> for MAP in mapmap( (1, 2, 3), (1., 2., 3.), () ):
            ...     print(*MAP, end='|\n')
            ...
            1 2 3|
            1.0 2.0 3.0|
            |
    '''
    return map(partial(map, function), iterables)

def mapparallel(functions, compounditerable):
    '''Parallel mapping. Conceptually, compounditerable
    represents a table, where each element is a "row" of the
    table. The functions are applied to the corresponding
    "column" of the table. Example: list(mapparallel([str, hex,
    bin], [(0,0,0), (1,1,1), (2,2,2)])) returns [['0', '0x0',
    '0b0'], ['1', '0x1', '0b1'], ['2', '0x2', '0b10']]'''
    return map(partial(zipapply, functions), compounditerable)

def mapchain(iterable, *functions): ###
    '''Returns the result of successive map-pings (sucessive
    function application).  Example: list(mapchain(['0.', '1.'],
    float, int, hex)) returns ['0x0', '0x1']'''
    from functools import reduce
    return reduce(lambda x, f: map(f, x), functions, iterable)

def persistent_map(function, iterable): ###
    '''Usage (e.g.):
        pmap = persistent_map(hex, range(3))
        print(*pmap())
        print(*pmap()) # second call to pmap() produces another map.
     '''
    from functools import partial
    return partial(map, function, iterable)

def onetomany(functions, iterable): #TAGS: multifunction apply
    '''Returns a map that produces one tuple per item produced
    by the iterable. Each item of a tuple is the result of
    applying the corresponding function to the item of the
    iterable. Example:
        >>> tuple(onetomany((str, hex), range(3)))
        (('0', '0x0'), ('1', '0x1'), ('2', '0x2'))
    '''
    return map(unstar(multifunction)(functions), iterable)

