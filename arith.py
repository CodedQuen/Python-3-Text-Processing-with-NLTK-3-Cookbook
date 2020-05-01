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

def square(x): ####
    '''Returns the square (product of a number with itself) of
    the argument.'''
    return x * x

def idivmod(dividend, divisor):
    '''Integer division. Returns a tuple containing the quotient
    and remainder.'''
    assert isinstance(dividend, int)
    assert isinstance(divisor, int)
    return dividend // divisor, dividend % divisor

def idivup(dividend, divisor):
    '''Integer division. Returns the quotient, rounded up.
    Example: idivup(10, 3) == 4'''
    dm = idivmod(dividend, divisor)
    return first(dm) + bool(second(dm))

def rangestoplacevalue(rngs):
    '''Given a sequence of integers representing the range of values for a
    variable-base number, returns the corresponding place values.

    Examples:

    rangestoplacevalue((10,6,10,6)) (e.g., seconds and minutes of a clock)
    returns [1,10,60,600] (e.g., the time 59:59 has a value of 1 * 9 + 5 * 10 +
    9 * 60 + 5 * 600)
    '''
    if not len(rngs):
        return []
    lst=[1]
    for item in enumerate(rngs[:-1]):
        lst.append(lst[first(item)]*second(item))
    return lst

def product(*args):
    '''HISTORY 2018-09-30: rewrote to exit early when
    zero-factor is encountered; 2018-09-28: formerly took a
    single interable argument: to get same behavior, do
    unstar(product)(iterable)'''
    from functools import reduce
    fore = []
    return reduce(
        lambda x, y: x * y,
        chain(
            quota(
                args,
                n=-1,
                criterion=ident, # i.e., quit at zero
                forerunner=fore),
            fore),
        1)

def scale(iterable, factor=1): #TO DO: Move to more appropriate location
    return map(partial(product, factor), iterable)

def dot(*iterables):
    '''returs the dot product of the iterable objects in
    iterables. Not intended to take a null
    list, list containing a single list, or list of list of different lengths.
    Example: dot([(1,2),(3,4)]) returns 11 = 1 * 3 + 2 * 4'''
    return sum(arrayproduct(*iterables))

def quotient(dividend, divisor):
    '''Returns the quotient. 0. and -0. are treated as
    arbitrarily small values for the purpose of evaluating
    division by "zero." Test:
for divisor in (-Inf(), -1., -0., 0., 1., Inf(), NaN()):
    for dividend in (-Inf(), -1., -0., 0., 1., Inf(), NaN()):
        try:
            q = quotient(dividend, divisor)
            q = repr(q)
        except:
            q = 'ERROR'
        print(dividend, '/', divisor, ':', q)
    '''
    from math import isnan
    if not divisor:
        if isnan(dividend) or not dividend:
            return NaN()
        else:
            return sign(dividend) * sign(divisor) * Inf()
    return dividend / divisor

reciprocal = partial(quotient, 1)

def itemeq(s, t):
    '''Compares for equality the corresponding items of subscriptable arguments
    sub1 and sub2'''
    if len(s) != len(t):
        return False
    for item in zip(s,t):
        if first(item) != second(item):
            return False
    return True

def powers(x, n=1):
    return map(lambda y: x ** y, range(n))

def divisible(n, divisor):
    assert isinstance(n, int), 'n must be int.'
    assert n, 'n must be positive.'
    assert isinstance(divisor, int), 'divisor must be int.'
    assert divisor, 'divisor must be positive.'
    return not bool(n % divisor)
