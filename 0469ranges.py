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



def ranges_contiguous(stops_iterable):
    '''returns a map of contiguous ranges. The stop of each
    range is given by the stops_iterable The stop of each item
    of the return matches the start of the next item of the
    return.

    **** ONLY THE INITIAL **** portion of the argument that is
    strictly increasing is used, in keeping with the name of the
    function ("-contiguous").

    REMINDER: if a set of ranges not beginning with range(0, x)
    is desired, the first item yield-ed may be disposed of
    (e.g., using rest).

    >>> tuple(ranges_contiguous((1, 3, 5, 8)))
    (range(1, 3), range(3, 5), range(5, 8))
    >>> tuple(ranges_contiguous((42, 3, 5, 8)))
    (range(0, 42),)
    '''
    deq = deque((0, 0))
    for k in iter(stops_iterable):
        if k <= deq[1]:
            return
        yield range(*shiftinv(deq, k))

