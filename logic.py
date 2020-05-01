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
def notall(iterable):
    return any(map(un(bool), iterable))

def comprest(seq, comp=equal):
    '''compares the first item in the sequence to the other items in the
    sequence.'''
    ret = []
    if len(seq) < 2:
        return ret
    for item in seq[1:]:
        ret.append(comp(first(seq), item))
    return ret

def compevery(seq, comp=equal):
    'STATUS: IN PROGRESS. compares items within sequence to one another.'
    return None
    '''
    ret = []
    for item in seq:
        ret.append([None]*len(seq))
    from itertools import permutations
    for p in permutations(range(len(seq)), 2):
        ret[][]
    for a in enumerate(seq):
        for b in seq:
            ret[first(a)].append(comp(second(a), b))
            #print(a, b, ret)
    return ret
    '''
