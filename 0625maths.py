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



def less(x, y=0): ###
    '''Returns whether x < y. HISTORY 2018-11-13: defined
    default value for y (arg 1).'''
    return x < y

def greater(x, y=0): ###
    '''Returns whether x > y.
    '''
    return x > y

def NaN(): ###
    '''Returns the float-ing point value NaN.'''
    return float('nan')

def Inf(): ###
    '''Returns the float-ing point value Inf. -Inf() returns the
    floating-point value -Inf.
    '''
    return float('inf')

def constant(obj=1): ###
    '''Returns a function that returns the argument used to call
    constant. The function returned by constant absorbs any
    number of arguments, doing nothing with them.
    '''
    def inner(*args, **kwargs):
        return obj
    return inner

def isint(obj): ###
    '''Returns a bool that indicates whether the single argument
    is an int.
    '''
    return isinstance(obj, int)

def isfloat(obj): ###
    '''Returns a bool that indicates whether the single argument
    is a float.
    '''
    return isinstance(obj, float)

