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
# Trivial Functions
# Dependencies: Python 3 built-ins

ITER_EMPTY = iter(()) # ONE SYMBOL INSTEAD OF FIVE

def nop(*args, **kwargs): ###
    '''Receive any arguments. Do Nothing. Return None. Intended
    use: testing.'''
    printerr('triv00.py: nop')
    pass

def NoneYet(*args, **kwargs): ###
    '''Intended usage: yield NoneYet, item is NoneYet, etc.'''
    assert False, 'Do not call. Intended use: object is NoneYet.'


def sign(x): ###
    from math import copysign
    return copysign(1, x)

def fnin(container, item): ###
    return item in container

def append(appendable, item): ###
    '''Returns appended *IN PLACE* appendable with item.'''
    appendable.append(item)
    return appendable

def extend(extendable, iterable): ###
    '''Returns extended *IN PLACE* extendable with item.'''
    extendable.extend(iterable)
    return extendable

def extendstep(appendable, iterable): ###
    '''Returns appendable *IN PLACE* appended with next item
    from iterable, if it is available.'''
    item = next(iter(iterable), NoMore)
    return appendable if item is NoMore else append(appendable, item)

fnappend = append #DEPRECATED use append

def fnzip(*args): ###
    return zip(*args)

def fnzipc(compounditerable): ###
    return zip(*compounditerable)

def fnis(a, b): ###
    return a is b

def fnnot(x): ###
    'returns (not x)---function version of keyword not'
    return not x

def negate(x): ###
    return -x

def alwaysTrue(*args, **kwargs): ###
    return True

def alwaysFalse(*args, **kwargs): ###
    return False

def alwaysneg1(*args, **kwargs): ###
    return -1

def lessorequal(x, y):
    return less(x, y) or equal(x, y)

def greaterorequal(x, y):
    return greater(x, y) or equal(x, y)

'''
def notequal(x, y): # REMOVED. Use un(equal) instead
'''
