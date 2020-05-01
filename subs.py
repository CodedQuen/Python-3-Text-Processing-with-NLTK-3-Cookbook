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
# EXTENSIONS FOR SUBSCRIPTABLE OBJECTS

'''
def swap01(lst) #REMOVED use swap
'''

def index_natural(sequence, index):
    '''Returns the nonnegative index into the sequence, given
    the integer index (negative or nonnegative).'''
    sequence[index] # POSSIBLY RAISE ERROR
    return index + len(sequence) if index < 0 else index

def getitem(sub, index=0):
    return sub[index]

member = getitem #DEPRECATED use getitem

def getitemnice(obj, index=0, nicevalue=None):
    '''HISTORY 2018-11-29: reworked for enhanced flexibility;
    now works with dict-s as well as list-like objects.'''
    try:
        item = obj[index]
    except:
        item = nicevalue
    return item

nicemember = getitemnice #DEPRECATED use getitemnice

def members(sequence, indices=None, nnn=(1,)): #.#
    '''Returns a map of the items in the sequence, per the
    indices (or, if indices is unspecified, nnn). DEPRECATED:
    the nnn parameter; use indices instead.'''
    return map(partial(member, sequence), nnn if indices is None else indices)

def membersets(sub, iterable):
    return mapchain(iterable, partial(members, sub), tuple)

def getitemsnice(sub, indices=(0,), nicevalue=None):
    return map(partial(getitemnice, sub, nicevalue=nicevalue), indices)

def yielditems(obj, indices=(), default=None):
    for index in indices:
        try:
            item = obj[index]
        except:
            item = default
        yield item

def getitems(obj, indices=(), default=None):
    '''Returns as a tuple the items of obj specified by the indices.'''
    return tuple(yielditems(obj, indices, default))


def PLACEHOLDER(sub): # old first
    try:
        len(sub)
        if len(sub):
            return sub[0]
        else:
            return None # 2017-12-22
    except:
        return sub # the argument has no length attribute, so the first one is the thing itself

def second(x, default=None):
    if not isiterable(x):
        return default
    return nextafter(chain(iter(x), (default,) * 2), 1)

def PLACEHOLDER(sub): ### old second
    if len(sub) > 1:
        return sub[1]

def REMOVEDrest(seq): # old name: rest see also: rest
    assert False # old
    return seq[1:]

def which(sub):
    'cf. which in R'
    return map(first, filter(_second, enumerate(sub)))

def penultimate(sequence, default=None, rangecheck=False):
    '''Returns the second-to-last item from the sequence.
    HISTORY 2018-12-03 enhanced flexibility. now optionally
    raises index-out-of-range error if rangecheck=True and that
    is the case.'''
    return \
            sequence[-2] if rangecheck else \
            default if len(sequence) < 2 else \
            sequence[-2]


'''You should never have to reach down beyond the second item on the stack---not
now, anyway---later, maybe.---Charles Moore (paraphrase, FIG meeting 20XX)'''

def eq(sub):
    if len(sub) < 2:
        return None
    return first(sub) == second(sub)

def minus(sub):
    if len(sub) < 2:
        return None
    return second(sub) - first(sub)

def indexnice(sub, item, default=-1): ###
    try:
        return sub.index(item)
    except:
        return default

def indexrvs(sub, n):
    '''Given an index into subscriptable object sub, returns a
    reversed index, i.e., the position from the end of sub.'''
    return len(sub) - n - 1

"""
#STATUS IN DEVELOPMENT. PROBLEM: 'gen' functions are in
generators.py, which needs this file, and this function need
generators.py
def indexcomp(sub, compar=notequal, default=-1):
    '''Returns the index of the first pair of consecutive items
    in sub for which compar returns True. The first pair has
    index 0. Can be use to "cut" a deque, split a list, etc. If
    there is no such index, returns the value specified by
    default.'''
    if len(sub) < 2:
        return default
    i = 0
    for pair in genlag(asgen(sub)):
        if compar(first(pair), second(pair)):
            return i
        i = i + 1
    return default
"""   
    
'''
def duplicates(sub): REPLACED WITH duplicates(iterable)
'''

def ismemberof(sub1, sub2):
    '''Returns a tuple of bools aligned with sub2, the values of
    which indicate whether the corresponding elmeent of sub2 is
    equal to an item in sub1.'''
    from functools import partial
    return tuple(map(partial(fnin, sub1), sub2))

def intersection(sub1, sub2):
    from functools import partial
    s1 = tuple(sub1) # needed so that sub1 may be a map
    return unique(reduce(lambda x, y: x + ([], [y])[y in s1], sub2, []))

def union(sub1, sub2):
    return unique(sub1 + sub2)
