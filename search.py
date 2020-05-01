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
def bsearch_lt(sseq, key, subdomain=None): ###
    '''Finds a sequence of indices in the subdomain of sorted sequence sseq.
    Uses "less than" to compare the key with values in the
    sequence.  Returns d, a duple of sequential int-s, such that
    sseq[d[0]] <= key <= sseq[d[1]]. Exceptions: d == (None,
    None) if key < sseq[0] or key > sseq[-1]. If the optional subdomain
    argument is given, only the corresponding range of sseq will
    be searched; subdomain has an interpretation similar to that
    of the returned value: sseq[subdomain[0]] <= key <=
    sseq[subdomain[1]]. '''
    #printerr('bsearch_lt: sseq, key, subdomain:', sseq, key, subdomain)
    def _bsearch(sseq, key, subdomain):
        'helper function'
        lo, hi = subdomain
        if hi - lo < 2:
            return subdomain
        mid = sum(subdomain) // 2
        if key < sseq[mid]:
            return _bsearch(sseq, key, (lo, mid))
        return _bsearch(sseq, key, (mid, hi))

    if not len(sseq):
        return (None, None)
    if len(sseq) == 1:
        return _bsearch(sseq, (0, 0), key)
    if subdomain is None:
        subdomain = 0, len(sseq) - 1
    if (key < sseq[subdomain[0]]) or (sseq[subdomain[1]] < key):
        return (None, None)
    return _bsearch(sseq, key, subdomain)

def lsearch(function=None, iterable=()):
    '''Similar to filter, except that the returned iterator has
    *AT MOST* one item. HISTORY: 2018-08-29, 2018-05-17:
    complete revision of old version.'''
    return quota(filter(function, iterable))


def enumerate_from(iterable, whence=0):
    ''''''
    assert False, '''untested. The whence feature seems already to
    be part of enumerate, but it is not documented in the help.'''
    return map(unstar(lambda n, item: (whence + n, item)), enumerate(iterable))

def lsearches(function_iterator=iter(()), iterator=iter(())): #TAGS parallel multiple
    '''Intended for searching through two separate, sorted
    iterators. Searches item by item through iterator for an
    item matching the first function produced by
    function_iterator. Then searches through the REMAINING items
    produced by iterator for the second function produced by
    function_iterator. The search ends when either
    function_iterator or iterator is exhausted. If not all
    functions match an item, the results may be nonintuitive.

    EXAMPLES:

    print(*lsearches(
        map(lambda n: lambda i: i == n, (1, 2, 3, 5, 8, 13, 21)),
        indefinite()))
    #(0, 1, 1) (1, 2, 2) (2, 3, 3) (3, 5, 5) (4, 8, 8) (5, 13, 13) (6, 21, 21)
    print(*lsearches(
        map(lambda n: lambda i: i == n, words('robert bruce timothy ware')), 
        iter(words('robert the bruce timothy ( kalistos ) ware'))))
    (0, 0, 'robert') (1, 2, 'bruce') (2, 3, 'timothy') (3, 7, 'ware')
    '''
    mold = -1
    for n, function in enumerate(function_iterator):
        printerr('lsearches: searching for item #', n, sep=NULL)
        for m, item in enumerate(iterator, 1 + mold):
            printerr('lsearches: testing against item:', item)
            if function(item):
                printerr('lsearches: for (inner): n, m, item', n, m, item)
                yield n, m, item
                mold = m
                break

def lsearches_by_value(value_iterator=ITER_EMPTY, iterator=ITER_EMPTY):
    '''Similar to lsearches, but compares values directly (via
    equality) rather than applying functions to the values
    found.
    print(*lsearches_by_value(
        iter((1, 2, 3, 5, 8, 13, 21)),
        indefinite()))
    (0, 1, 1) (1, 2, 2) (2, 3, 3) (3, 5, 5) (4, 8, 8) (5, 13, 13) (6, 21, 21)
    print(*lsearches_by_value(
        iter(words('robert bruce timothy ware')), 
        iter(words('robert the bruce timothy ( kalistos ) ware'))))
    (0, 0, 'robert') (1, 2, 'bruce') (2, 3, 'timothy') (3, 7, 'ware')
    ''' 
    return filter(None, lsearches(
        map(
            lambda sought:
                    lambda found: second(
                        printerr('lsearches_by_value: lambda (inner):'
                                ' sought, found:', sought, found),
                        found == sought),
            value_iterator),
        iterator))








''' # KEEP FOR REFERENCE
def lsearch(iterable, key, compar=lambda x, y: x == y, default=None):
    # HISTORY 2018-05-17: REMOVED. Returns the first item in
    # iterable where compar(key, item) == True. Returns default
    # if there is no such item.  Originally intended that
    # iterable is a generator so that multiple calls to lsearch
    # may start searching where the previous search left
    # off---requires appropriately orderd keys.
    for item in iterable:
        if compar(key, item):
            return item
    return default
'''

def search_each(sseq, keys, srch=bsearch_lt): #.#
    '''Searches for each key of keys, within sseq. Both sseq and
    keys are expected to be sorted in ascending order. Yields
    the resulting interval (a duple of values indicating the two
    ajacent values in sseq wich a key is between).'''
    from functools import partial
    search = partial(srch, sseq)
    # commented out parts to narrow dom at each step---seems like effor to compute dom is not worth it.
    #dom = 0, len(sseq) - 1 # initial domain: all members of sseq
    for k in keys:
        where = search(k) #, subdomain=dom)
        #printerr('search_each(B): k, where, dom:', k, where, dom)
        yield where
        #dom = (where[0], dom[0])[where[0] is None], dom[1]
