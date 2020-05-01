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



def lfilter(collection, function=ident):
    '''returns a tuple consisting of the elements of the
    argument, except those initial elements which do not pass
    the test function. Cf. filter, str.lstrip.
    '''
    deq = deque(collection)
    while deq and not function(deq[0]):
        deq.popleft()
    return tuple(deq)

def rfilter(collection, function=ident):
    '''returns a tuple consisting of the elements of the
    argument, except those final elements which do not pass
    the test function. Cf. filter, str.rstrip.
    '''
    deq = deque(collection)
    while deq and not function(deq[-1]):
        deq.pop()
    return tuple(deq)

def lrfilter(collection, lfunction=ident, rfunction=None):
    '''same as applying rfilter with rfunction on the return of
    applying lfilter with lfunction. If rfunction is None (the
    default), lrfilter behaves as if rfunction == lfunction.
    '''
    if not rfunction:
        rfunction = lfunction
    return rfilter(lfilter(collection, lfunction), rfunction)

