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
# Extensions for deque-s and other popleft-able and
# appendleft-able objects
# Dependencies INCLUDE: deque from collections

def shiftinv(deq, value): ### tag: ASL left shift <<
    '''Modifies *IN PLACE* the deque deq by appending the value,
    then removing the left item. Returns the modified deque.
    HISTORY: 2018-10-05 formerly would fail if deq had no
    elements.'''
    assert deq.append and deq.popleft
    return popleft(append(deq, value))

def shiftin(deq, iterable): ### tag: ASL left shift <<
    '''Returns a modified *IN PLACE* version of deque deq, where
    items have been shifted to the left, the item origially at
    the initial position has been removed, and a new item (if
    available from iterable) has been appended. c.f.
    deque.extend. TO DO: when shiftout needed: refactor to
    shift, shiftin, shiftout.'''
    for item in iterable:
        shiftinv(deq, item)
        break
    return deq

