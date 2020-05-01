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



rangeof = compose(range, len)
rangeof.__doc__ = ('Returns a range object over the indices of'
    'the argument.')

def range1(n): ###
    'Returns a range object which is capable of producing n consecutive int-s, starting with int(1).'
    assert isinstance(n, int)
    return range(1, 1 + n)

def rangeincl(*args):
    msg = ('too ', '', ' arguments: stop | (start, stop [,step]).')
    l = len(args)
    assert l > 0, msg[0] + 'few' + msg[2]
    assert l < 4, msg[0] + 'many' + msg[2]
    assert all(map(isint, args)), 'All arguments must be int-s.'
    if l == 1:
        return range(1 + first(args))
    if l == 2:
        return range(*sums(zip(args, (0,1))))
    return range(*sums(zip(args, (0,1,0))))

def rangestar(*args):
    return range(*args)

def ranges(iterable):
    '''The argument produces iterables of values up to a count
    equal to the maximum acceptable to the range function.
    Returns a map of range-s conistent with the input.'''
    return map(unstar(range), iterable)

def partition(iterable):
    '''Originally intended to return a map of range-s whose
    items, if chain-ed, form an iterator of the integers
    beginning with the first value in iterable and ending with
    one less than the last value in iterable (consistent with
    range). This will be the case if the items in iterable are
    strictly increasing integers. Example:
    >>> print(tuple(partition((-7, -3, -1, 0))))
    (range(-7, -3), range(-3, -1), range(-1, 0)
    >>> print(*map(tuple, partition((-7, -3, -1, 0))))
    (-7, -6, -5, -4) (-3, -2) (-1,)
    '''
    return ranges(running(iterable))
    
def rangezn(*stops):
    '''Returns a range in Z^n. Example: '''
    return stops

