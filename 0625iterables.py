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



def tuplefilter(function_or_None, iterable):
    '''Shorthand for tuple(filter(...))'''
    return tuple(filter(function_or_None, iterable))

def tuplemap(function, *iterables):
    '''Shorthand for tuple(map(...))'''
    return tuple(map(function, *iterables))

def tuplezip(*iterables):
    '''Shorthand for tuple(zip(...))'''
    return tuple(zip(*iterables))

def maxlen(compound_iterable):
    '''Returns the len of the longest inner iterable in the
    compound_iterable, or zero if the compound_iterable is
    empty.
    '''
    return max(chain((0,), map(len, compound_iterable)))

def textcolumnwidth(string_iterable):
    '''Returns the max len of the strings in the
    string_iterable. The str-s therein are taken **** AS IS ****
    and there is no stripping of whitespace, for example.
    '''
    return maxlen(string_iterable)

