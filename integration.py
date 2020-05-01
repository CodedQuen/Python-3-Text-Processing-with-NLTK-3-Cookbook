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
def area(p): # tags: integrate integration trapezoidal rule
    '''Returns the area under the line segment represeted in
    Cartesian coordinates by the duple of duples p. This
    function is consistent with the Trapezoidal Rule. Example:
    cartareaunderlinesegment(((0, 0), (1, 1))) returns 0.5'''
    return (p[1][0] - p[0][0]) * (p[1][1] + p[0][1]) / 2 # (x2 - x1) * (y2 + y1) / 2

def piecewise_linear_integral(p): # tags: integrate integration trapezoidal rule
    '''Returns the area under the continuous, piecewise linear
    curve represented by the argument. The argument is a
    sequence (could be tuple or iterator, or ?) of duples, each
    item of which is either a float or int.  ASSUMPTION: ordered
    pairs are sorted in order of increasing "x" value.'''
    dbl = iter_double(p) # representative sequence: 1 1 2 2 ... n n
    next(dbl, None) # 1 2 2 3 3 ... l l m m n n
    return sum(map(area, fullgroups(dbl))) # fullgroups: 1 2   2 3   ...   l m   m n

def gen_save_first_last(lst, iterator):
    '''Yields the items in iterator, but saves in the list lst
    the first and last items yield-ed. lst is modified *IN
    PLACE*.'''
    # next 4 lines: initialize lst
    listclear(lst)
    obj = object() # unique object
    lst.append(obj)
    lst.append(obj)
    for i in iterator:
        lst[0] = i
        yield i
        break
    for i in iterator:
        lst[1] = i
        yield i
    # final lines: clean-up needed for iterators of 0 or 1 items
    if lst and lst[-1] == obj:
        lst.pop()
    if lst and lst[-1] == obj:
        lst.pop()

def mean_value_piecewise_linear(iterator):
    '''Returns the mean value of the continuous piecewise linear
    function represetned by the iterator argument (sequence of
    ordered pairs). Each item of the iterator is a duple, each
    item of which is either a float or int. Example:
    mean_value_piecewise_linear(iter(((0,0), (1,1), (2,0))))
    returns 0.5. ASSUMPTION: ordered pairs are sorted in order
    of increasing "x" value.'''
    p = []
    a = piecewise_linear_integral(gen_save_first_last(p, iterator)) # area
    w = p[1][0] - p[0][0] # width
    if w:
        return a / w
    return 0 # zero-width ==> zero area
