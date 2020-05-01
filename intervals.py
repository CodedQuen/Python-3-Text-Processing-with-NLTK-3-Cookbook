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
def interval(x, pos=0, width=1): ###
    '''Given an interval width (unit), a value (x), an a
    relative position (pos) of that value within the interval,
    returns a tuple representing that interval. The return is
    distinct from the typical mathematical definition of
    interval in that there is no information about whether
    either boundary is open or closed.'''
    return x - pos * width, x + (1 - pos) * width

def intervals(iterable, pos=0, width=1):
    '''Returns a map of intervals (see def interval) of width
    width, where the elements of iterable are at relative
    position pos within each interval.'''
    return map(partial(interval, pos=pos, width=width), iterable)

def withinintervalo(option, inter=(0, 1), value=0.5):
    return {'l': betweenl, 'r': betweenr, 'i': betweeni, 'x':
            betweenx}[option](first(inter), value, second(inter))

withinintervall = partial(withinintervalo, 'l')
withinintervalr = partial(withinintervalo, 'r')
withinintervali = partial(withinintervalo, 'i')
withinintervalx = partial(withinintervalo, 'x')

def lsearchintervals(inter, value, fnwithin=withinintervalr):
    '''Advances the iterator inter (which produced duples of
    numeric values representing intervals) until exhausted or
    until value is found in one of the intervals produced.
    Returns a duple containing the item number and the interval
    itself, or an empty tuple in the case where value was not
    found within any interval.'''
    fn = partial(fnwithin, value=value)
    return tuple(lsearch(lambda x: fn(second(x)), enumerate(inter)))
