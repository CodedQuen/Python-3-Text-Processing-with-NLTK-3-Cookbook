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

def count(iterable, store=None):
    '''Returns the number of items in iterable. If iterable is
    an iterator, it is modified *IN PLACE*, and is exhausted if
    finite. FUTURE: items will be stored in the store object by
    store.append. HISTORY: 2018-03-16: redesigned with
    correction (was returning one less than count).
    '''
    return sum(map(constant(1), iterable))

