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


def isindexed(obj): ###
    '''Returns a bool indicating whether the item is indexed,
    i.e., whether obj[i] is a valid operation.
    '''
    return hasattr(obj, '__getitem__')

def last(sequence): #.#
    '''Returns the last item of a sequence, sequence[-1].
    However, returns None if there is no last item, i.e., if the
    sequence is empty.'''
    if isindexed(sequence) and sequence:
        return sequence[-1]

