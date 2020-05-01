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

def first(iterable, default=NoMore):
    '''Returns the first item of arg0.  If arg0 is an iterator,
    advances it *IN PLACE* if there are any items remaining;
    returns default no items remain. Returns arg0 itself if it
    is neither indexable nor iterable.'''
    if isindexed(iterable) and iterable:
        return iterable[0]
    elif isiterable(iterable):
        return next(iter(iterable), default)
    else:
        return obj

