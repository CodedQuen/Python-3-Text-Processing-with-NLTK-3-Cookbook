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
# FUNCTIONS FOR SEQUENCES

def rangecheck(sequence, index):
    try:
        sequence[index]
        return True
    except:
        return False

def pad(sequence, n, item_sequence=(None,)):
    '''In the trivial case,  n <= len(sequence), returns
    tuple(sequence).  Otherwise, returns a tuple of length n
    whose left elements are taken from the item_sequence. Items
    are recycled if needed to obtain the quantity required.
    '''
    return \
        tuple(reversed(tuple(quotan(
            recycle(tuple(reversed(item_sequence))),
            max(0, n - len(item_sequence)))))) + \
        tuple(sequence)

def seqindex(seq, x): ###
    if x in seq:
        return seq.index(x)

def flatlist(seq):
    from functools import reduce
    return reduce(lambda x, y: x + list(y), seq, [])

def tidied(seq): #TAGS: sort sorted
    l = list(seq);   l.sort();   return l

def flipped(seq): #TAGS: reverse swap, related:sort
    l = list(seq);   l.reverse();   return l
