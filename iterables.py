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

# FUNCTIONS OF ITERABLES

def triangular(iterator):
    '''Returns a map of tuples. Each tuple contains the next 1,
    2, 3, ... items from the iterator. The length of the last
    item produced by the return (nonzero) depends upon how
    many remaining items are available.
            >>> for row in triangular(quota(indefinite(), 8)):
            ...     print(*map(partial(str.format, '{0:2d}'), row))
            ...
             0
             1  2
             3  4  5
             6  7
    '''
    m = map(partial(nextgroup, iterator), indefinite(1))
    return iter(lambda: next(m), ())

def triangularindices(nrow):
    '''Returns an iterator that produces the (little endian;
    fastest-first) indices of a triangular matrix:
    (0, 0),
    (0, 1), (1, 1),
    (0, 2), (1, 2), (2, 2), ...
    '''
    for i in range(nrow):
        for j in range(1 + i):
            yield j, i

def triangularindices1(nrow): #TAGS iterator
    '''Returns an iterator that produces the "faster" indices of
    a triangular matrix:
    0,
    0, 1,
    0, 1, 2, ...
    '''
    return map(first, triangularindices(nrow))

def triangularindices2(nrow): #TAG iterator
    '''Returns an iterator that produces the "slower" indices of
    a triangular matrix:
    0,
    1, 1,
    2, 2, 2, ...
    '''
    return map(second, triangularindices(nrow))

def filterbytag(function=first, iterable=((False, None),)):
    '''Similar to filter, except the function defaults to first.
    Intended for use with iterables that produce sequences
    (e.g., tuples). Example: see whitespaces'''
    return filter(function, iterable)

def wherein(compound_iterable, item):
    '''Returns a map if integer indices which tell where the
    item is found. Each of the iterables produced by
    compound_iterable must be finite.
            >>> tuple(wherein([{1}, {}, {1}], 1))
            (0, 2)
    '''
    return mapchain(
        filteriterables(
            renumerate(map(
                lambda iterable: item in iterable,
                compound_iterable))),
        tuple,
        first)

def renumerate(iterable, index=0):
    '''Similar to enumerate, except that the item and item
    number are in reverse order. Numbering begins with index.'''
    return mapchain(enumerate(iterable, index), reversed, tuple)

def mergesort(iterator0, iterator1, key0=None, key1=None):
    key1 = ident if key1 is None else key1
    key0 = ident if key0 is None else key0
    v0, v1 = next(iterator0, NoMore), next(iterator1, NoMore)
    k0, k1 = None if v0 is NoMore else key0(v0), \
             None if v1 is NoMore else key1(v1)
    while (v0 is not NoMore) and (v1 is not NoMore):
        k0_lt_k1 = k0 < k1
        yield v0 if k0_lt_k1 else v1
        if k0_lt_k1:
            v0 = next(iterator0, NoMore)
            k0 = None if v0 is NoMore else key0(v0)
        else:
            v1 = next(iterator1, NoMore)
            k1 = None if v1 is NoMore else key1(v1)
    while v0 is not NoMore:
        yield v0;   v0 = next(iterator0, NoMore)
    while v1 is not NoMore:
        yield v1;   v1 = next(iterator1, NoMore)

def issorted(iterator):
    '''Modifies iterator *IN PLACE*. Tells whether the values
    produced by the iterator are sorted. On return, the iterator
    is left in an indeterminate state. The "<" operator must be
    defined for consecutive items of the iterator which are in
    order, and for the first pair of items which are out of
    order, if that situation occurs.'''
    after = next(iterator, NoMore)
    while True:
        before = after
        after  = next(iterator, NoMore)
        if after is NoMore:
            return True
        if after < before:
            return False

def reordered(iterable, dictionary): ###
    '''Returns the items of the iterable as a tuple, in the
    order specified by dictionary. The dictionary items are
    int-int pairs where the key refers to the corresponding item
    produced by the iterable and the value refers to the index
    in the return. Typical errors might be 'tuple index out of
    range' or 'list assignment index out of range' in the case
    of mismatches Example: reordered((2,29,2000), {0:1, 1:2,
    2:0}) returns (2000, 2, 29)'''
    t = tuple(iterable);   l = list(t)
    for key in dictionary.keys():
        l[dictionary[key]] = t[key]
    return tuple(l)

filter1 = partial(filter, None)

def filteruntil(function, iterator): #TAGS: next
    '''Advances the iterator *IN PLACE* until 1) function(item)
    is true or 2) the iterator is exhausted. Returns either an
    empty iterator (case 2) or an iterator that produces the
    first value in iterator for which function(iter) is true,
    followed by the remaining items in iterator. See also:
    filter. HISTORY: iterator was formerly an iterable.
    Example:
            >>> next(filteruntil(isgraph, iter(('\n', '\t', 'W', 'O', 'R', 'D'))))
            'W'
            >>> next(filteruntil(isgraph, iter(())), NoMore)
            <function NoMore at 0x02279108>
    '''
    item = next(filter(function, iterator), NoMore)
    return chain(() if item is NoMore else (item,), iterator)

def filteriterables(compound_iterable):
    '''Similar to filter, but passes the rest of the items of
    each iterable, provided that the initial item of the
    iterable is True. Example:
        >>> f = filteriterables(((False, 'False'), (True, 'True')))
        >>> tuple(next(f))
        ('True',)
    '''
    for iterable in iter(compound_iterable):
        it = iter(iterable)
        if next(it, False):
            yield it

def advancetoitem(iterator, key): #TAGS: next
    '''Advances the iterator *IN PLACE* until 1) an item equal
    to key is found or 2) the iterator is exhausted. Returns
    either an empty iterator (case 2) or an iterator that
    produces the first value in iterator equal to key, followed
    by the remaining items in iterator. See also: filteruntil.
    Examples:
            >>> it=iter(range(9)); it1=advancetoitem(it, 4); next(it1, NoMore)
            4
            >>> it=iter(range(9)); it1=advancetoitem(it, 99); next(it1, NoMore)
            <function NoMore at 0x0223AD68>
    '''
    return filteruntil(partial(equal, key), iterator)

def nextcluster(iterator, function, sep=[], n=None):
    '''A cluster is a sequence of like objects separated by one
    or more objects that are unlike those of the cluster. Whether
    an object belongs in a cluster is determined by evaluating
    function(item), where item is an object produced by the
    iterator.'''
    return tuple(quota(filteruntil(function, iterator), n=n,
            criterion=function, forerunner=sep))

def nextword(charactermap, function=isgraph, sep=[], n=None):
    '''Advances the charactermap *IN PLACE* past the next word
    (a sequence of characters, where function is true for all).
    The first character for which function is false is stored in sep.
        Example 1 (whitespace-separated words):
            >>> cm = iter('this is a test')
            >>> nw = partial(nextword, cm)
            >>> print(*iter(nw, None), sep='-')
            this-is-a-test
        Example 2 (fixed-width words, length 4):
            >>> cm = iter('this__is___atest')
            >>> nw = partial(nextword, cm, function=bool, n=4)
            >>> print(*iter(nw, None))
            this __is ___a test
        Example 3 (fixed-width words, length 6):
            >>> cm = iter('this__is___atest')
            >>> nw = partial(nextword, cm, function=bool, n=6)
            >>> print(*iter(nw, None))
            this__ is___a test
    '''
    return next(iter(
        partial(
            unstar(join),
            nextcluster(charactermap, function, sep, n)),
        ''))

def wordmap(charactermap, function=isgraph, n=None):
    '''Returns a map of words, given a character map. The
    meaning of the optional args function and n are as
    with nextword.
        Example 1 (words separated by whitespace):
            >>> cm = iter('The quick brown fox jumped over the lazy dog.')
            >>> wm = wordmap(cm)
            >>> print(*wm, sep='-')
            The-quick-brown-fox-jumped-over-the-lazy-dog.
        Example 2 (fixed-width words):
            >>> cm = iter('-128 127   1  -1   0')
            >>> wm = wordmap(cm, function=bool, n=4)
            >>> print(*wm, sep='\n')
            -128
             127
               1
              -1
               0
        Example 3 (structured text):
            >>> # PROBABLY WOULD NOT USE wordmap FOR A COMPLEX
            >>>         # CHARACTER SEQUENCE, THOUGH
            >>> cm=iter('#COMMENT\n 0 0 1 1 0 0 INSIGNIFICANT\n')
            >>> wm=wordmap(cm, function=partial(un(equal), '\n'))
            >>> next(wm)
            '#COMMENT'
            >>> wm=wordmap(cm, function=bool, n=2)
            >>> print(*quota(wm, 6)) # end-of-line marker processed as separator
             0  0  1  1  0  0
            >>> wm=wordmap(cm, function=partial(un(equal), '\n'))
            >>> next(wm)
            ' INSIGNIFICANT'
            >>> next(cm) # end-of-line marker processed as separator
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            StopIteration
            Example 4:

                
    f = open('p:/testfile-mf1.txt')
    rewind(f)
    cm = fcharactermap(f)
    wm = wordmap(cm, function=partial(un(equal), '\n'))
    pos = f.tell()
    next(wm)
        f.seek(pos)
    next(wm)
    next(wm)
    wm = wordmap(cm, function=bool, n=10)
    pos = f.tell()
    f.readline()
    f.seek(pos)
    tuple(quota(wm, 7))
    f.readline()
    tuple(quota(wm, 2))
    f.read(20)
    tuple(quota(wm, 3))
    f.readline()
    wm = wordmap(cm)
    print(*wm)

    '''
    return quota(
        map(
            partial(
                nextword,
                function=function,
                n=n),
            steady(charactermap)),
        n=None,
        criterion=bool)

def repeater(iterator, preupdate=None, postupdate=None):
    '''
    Tests:
    print(*quota(repeater(range(9)), 5)) # Test 1
    print(*quota(repeater(indefinite()), 42)) # Test 2
    print(*quota(repeater(indefinite(), function=None), 42)) # Test 2A
    
    
    # Test 3
    
    def preupdate(memo):
        memo['out'].append(memo['in'][-1] * 2)
        memo['yield!'][0] = True
    
    for item in quota(repeater(indefinite(), preupdate=preupdate), 42):
        print('', item, end='')
    
    
    # Test 4
    
    def preupdate(memo):
        if not memo['out']:
            memo['out'].append
        temp = memo['in'].pop()
        memo['out']
        memo['out'].append(memo['in'][-1] * 2)
        memo['yield!'][0] = True


    '''
    memo = {'in': deque(), 'out': deque(), 'yield!': [False]}
    if not preupdate:
        def preupdate(memo):
            memo['out'].append(memo['in'][-1])
            memo['yield!'][0] = True
    if not postupdate:
        def postupdate(memo):
            memo['in'].clear()
            memo['out'].clear()
    for item in iterator:
        memo['in'].append(item)
        preupdate(memo)
        if memo['yield!']:
            yield memo['out'][-1]
            memo['yield!'][0] = False
            postupdate(memo)

def recycle(sequence):
    '''Returns a map that produces the elements of sequence over
    and over again. Example:
            >>> hours = tuple(chain((12,), range1(11)))
            >>> print(*quota(recycle(hours), 24))
            12 1 2 3 4 5 6 7 8 9 10 11 12 1 2 3 4 5 6 7 8 9 10 11
    '''
    return map(sequence.__getitem__, cycle(len(sequence)))

def _zip_lazy(iterator_of_sequences,
        ragged=False, allow_skipping=False):
    '''FUTURE: ragged and allow_skipping provide for
    different-length items being produced by the primary
    argument and for subitems to be left un-yield-ed before
    getting the next subitem from the next item.
        See zip_lazy for additoinal documentation)
    '''
    FIRST = next(iterator_of_sequences, NoMore)
    yielded = [False] * len(FIRST)
    current = [FIRST]
    def inner(which):
        while True:
            if all(yielded):
                current[0] = next(iterator_of_sequences, NoMore)
                if current[0] is NoMore:
                    return
                assert len(current[0]) == len(FIRST), \
                        'Designed for each item to have same len-gth.'
                for i in rangeof(yielded):
                    yielded[i] = False
            assert not yielded[which], \
                    'Designed to yeild each item fewer than twice.'
            yielded[which] = True
            yield current[0][which]
    yield tuplemap(lambda i: inner(i), rangeof(FIRST))

def zip_lazy(iterable_of_sequences):
    '''Given an iterable of sequences, returns a tuple of
    iterators. The iterators of the tuple may be next-ed in any
    order to produce the values. The iterable argument may
    produce a finite or indefinite number of values. Example:
    (used in MF/Grids/resurf.py/)'''
    return next(_zip_lazy(iterable_of_sequences))

def zipgroups(*sequences_of_iterators): 
    '''Given one or more sequences of iterators, returns a zip
    object that produces the values from the iterators. Values
    are grouped into tuples accoding to their origin (i.e., from
    which iterator of which sequence). Originally developed for
    organizing data for applicaiton to sumproduct. Example:

        >>> # ALTERNATE LINE NUMBERING
        >>> print(
        ... *zipgroups(
        ...     (range(2), range(1, 3, 1)),
        ...     (('first line', 'second line'),)),
        ... sep='\n')
        ((0, 1), ('first line',))
        ((1, 2), ('second line',))
    '''
    return zip(*map(unstar(zip), sequences_of_iterators))

def substitute(iterable, test_function=lambda x:bool(x), subst_function=ident):
    '''Similar to filter, but uses subst_funciton to produce an
    item for items in iterable that fail the test_function.'''
    return map(
        lambda x: x if test_function(x) else subst_function(x),
        iterable)

def findevery(values, iterable):
    '''c.f. findall. Higher level find. Returns a dict where
    each item of values (arg 1) matches a key, and each value is
    a find-result (map of indices).'''
    ordering = tuple(iterable)
    return dictzip(values,
            map(partial(argswap(find), ordering), values))

def findunique(values, iterable):
    '''Returns a tuple of indices of values found in the
    iterable. The return is sorted.'''
    return tuple(sorted(list(set(flat(*findevery(values, iterable).values())))))

def found(values, iterable):
    '''Returns the values found in iterable.'''
    assert False, 'Placeholder'
    pass

def findmax(values, ordering):
    '''Returns the highest index of the values found in
    ordering.'''
    indices = findunique(values, ordering)
    return None if not indices else max(indices)


def more(iterator): # tags: next
    '''Return the next item produced by the iterator, if it
    exists.  Otherwise return NoMore.'''
    return next(iterator, NoMore)

def nmore(iterator, n):
    '''Return a tuple containing the next n items produced by
    the iterator. The tuple will contain fewer than n items if
    the iterator is exhausted before n items are prodced.'''
    l = [ more(iterator) for i in range(n) ]
    while l and l[-1] == NoMore:
        l.pop()
    return tuple(l)

def ascupper():
    from string import ascii_uppercase
    return tuple(ascii_uppercase)

def forceiter(x):
    '''Returns an iterator over the elements of x. If x is not
    iterable, return an iterator that produces x.'''
    return iter(
        x if hasattr(x, '__iter__') else (x,))
    #ABOVE: UPDATED 2019-02-20 (untested)
    #BELOW: CODE PRIOR TO 2019-02-20
    try:
        return iter(x)
    except:
        return iter((x,))

def enkey(key, iterable):
    '''Similar to enumerate, but rather than a count, the duples
    produced by the return contain the key corresponding to the
    item of iterable. Example:
            >>> print(*enkey(range(9), lambda x: x % 2))
            (0, 0) (1, 1) (0, 2) (1, 3) (0, 4) (1, 5) (0, 6) (1, 7) (0, 8)
    '''
    return map(lambda item: (key(item), item), iterable)

def redundant(iterable, n=2): # tags: repeat repetition copies duplicate replicate
    return chain(*map(lambda x: iter((x,)*n), iterable))

def interlace(*iterables):
    '''Returns a single, serialized iterator over the values
    produced from the parallel iterables. Like zip, the length
    of the return is controled by the shortest iterable.
    Example:
            >>> print(*interlace(range(26),
                    map(chr, range(65, 92))))
            0 A 1 B 2 C ...
    '''
    return chain(*zip(*iterables))

def separate(iterable, sep=' '):
    '''Returns an iterator over the items of iterable, where
    each one is separated by sep. Example:
            >>> ''.join(separate(('fourscore', 'years', 'and',
                    'seven')))
            'fourscore years and seven'
    However, that example is trivial, since you would use
    str.join to achieve the same end.
    '''
    return rest(interlace(iter(constant(sep), None), iterable))

def enumerate1(iterable):
    return enumerate(iterable, start=1)

def printenum(iterable, sep=': '):
    '''Pretty-print an enumerate-like object.'''
    for item in iterable:
        print(first(item), sep, second(item), sep=NULL)

def allbutlast(iterator, n=1):
    '''yield-s all but the last n items from iterator.'''
    if n < 0:
        return
    deq = deque(quota(iterator, 1 + n)) # seed the deque
    while n < len(deq):
        yield deq.popleft()
        item = next(iterator, NoMore)
        if item is NoMore:
            return
        deq.append(item)


def unique(iterable):
    '''Returns a set of the unique items in iterable. HISTORY
    2018-03-27: previously returned a list. This is now an alias
    for the set function.'''
    return set(iterable)

def inc(iterable):
    return map(lambda x: 1 + x, iterable)

def _reiterator_nof(store, iterator):
    'Helper function for reiterator'
    from tempfile import NamedTemporaryFile as ntf
    f = ntf('w+') # read and write mode
    tuple(filter(partial(store, f), iterator)) # tuple forces evaluation
    return rewind(f)

def reiterator(store, retrieve, iterator, staticfile=None):
    '''Returns a new iterator that reproduces the iterator (arg
    2).  The values underlying the reproduced iterator are
    stored in a temporary file according to the function store
    (arg 0), and retrieved according to retrieve (arg 1).
        However, if staticfile is specified, store and iterator
    are not used, but rather the new itertor is produced from
    the existing file *THAT WILL BE REWOUND* each iteration.
        It is intended that specializatoins of this function be
    produced using partial to curry the store and retrieve
    arguments.
        As presently implemented, if the store function returns
    values, it is possible that computer memory will be wasted
    during the storage process.
        NOTE. It is easy to construct a combination of store and
    retrieve functions that cause the reiterated values not to
    be representative of the original values underlying the
    iterator (arg 2). It is also not hard to pass an iterator of
    indefinite size to this function, and cause storage media to
    become overly utilized, perhaps even full.
        See tablereiterator in an acompanying Python 3 source
    file for example usage.
    '''
    f = staticfile if staticfile else _reiterator_nof(store, iterator)
    pos = f.tell()
    while True:
        yield retrieve(f)
        f = freset(f, pos)

class reiter: ### tags: reiter
    '''An iterator that can be partially rewound.
    .
    STATUS
    .
    HISTORY
    .
        2018-01-18: revised _retreat to be consistent with _advance.
                    added asiter ("as iter") method
        2018-01-17: revised peek to prevent StopIteration
        2018-01-16: corrected iteratoin capability.
                    revised _true_next
        2018-01-05: seems to work: passed cursory tests.
    .
    Potential Application: reading through a gigantic file or
    other data stream, where a partial history is needed for a
    calculation: maybe you want to compute a running average
    where there may be lots of missing data (variable record
    length), but there is a known maximum amount of data are
    needed for the calculation of the average (say there is
    15-minute data and one-day averages are being computed).
    .
    AUTHOR: D. Michael Parrish
    .
    ACKNOWLEDGMENT: Created using resources of the South Florida
    Water Management District.
    .
    LICENSE: Public Domain. Kindly acknowledge author and SFWMD
    if using for published work.
    REITERATOR
    .
    This script defines a reiterator class, which is similar to
    an iterator, but where previous items may be reviewed,
    within limits.
    .
    A concise description is given below---it was created using
    the Python function help(reiterator) after loading the
    present file to the Python. Source code follows. But first,
    a demo:
    .
    >>> with open('h:/folderpath/reiterator.py') as f:
    ...     exec(f.read())
    ...
    >>> re = reiterator(iter(range(9)))
    >>> re._state()
    {'deq': deque([<object object at 0x022D3BE0>, 0]), 'pos': -1, 'canditto': False}
    >>> # the "hidden" function _state returns a dict containing the
    >>> # important object attributes.
    >>> # The memory is stored in a deque named deq. The pos
    >>> # attribute stores the index of the next value.
    >>> # A unique object, null, is used as a null value. Its
    >>> # presence at position -2 in deq indicates that there is no
    >>> # history.
    >>> re.seek(-1)
    0
    >>> # seek returns 0 because it could not seek backwards by the
    >>> # indicated amount---there are no remembered items back
    >>> # there.
    >>> next(re)
    0
    >>> re.seek(-1)
    -1
    >>> # after doing a next, we can go back one step.
    >>> next(re)
    0
    >>> # we go the same value over again.
    >>> next(re)
    1
    >>> next(re)
    2
    >>> re.seek(-99)
    0
    >>> # we tried to go too far back; seek keeps us where we're at,
    >>> # and tells us so: zero indicating that the position moved
    >>> # zero places.
    >>> re.peek()
    3
    >>> # we look ahead. not surprisingly, the next value after 2
    >>> # will be 3.
    >>> re.seek(99)
    6
    >>> # we tried to go forward 99 places, but the iterator is
    >>> # exhausted before we can get there. seek tells us that we
    >>> # were allowed to advance 6 positions.
    >>> re.peek()
    <object object at 0x022D3BE0>
    >>> # the null value was returned because we have exhausted the
    >>> # iterator.
    >>> next(re)
    <object object at 0x022D3BE0>
    >>> re.null
    <object object at 0x022D3BE0>
    >>> # the null object can be accessed by the null attribute.
    >>> next(re) is re.null
    True
    >>> # you can test if the next item is the null value.
    >>> re.peek() is re.null
    True
    >>> # you can test if the null value will be returned when
    >>> # next is called.
    '''
    class obj:
        def __init__(self, st):
            self.s = str(st)
        def __repr__(self):
            return self.s
    '''pre and post are simply unique objects with a
    representation so that they may be displayed sensibly.'''
    pre  = obj("obj('reiter.pre')")
    post = obj("obj('reiter.post')")
    def _init_part_1(self, iterator, limit=1):
        '''Helper function for __init__. Allows attributes to be
        defined before they are referenced.'''
        self.iterator = iterator
        from collections import deque
        self.deq = deque([reiter.pre] * (1 + limit))
        self.pos = -1
    def _true_next(self):
        '''Helper function for __next__. This will be called
        because another value needs to be retrieved from
        self.iterator---the 'next' value has not yet been
        stored. The value of self.pos should be -1.'''
        assert self.pos == -1, 'ASSUMPTION of _true_next: self.pos == -1'
        if self.deq[-1] == reiter.post:
            raise StopIteration
        from itertools import chain
        shiftin(self.deq, astuple(next(self.iterator, reiter.post)))
        # The same value of self.pos now indicates the element
        # previously located to the right.
        return self.deq[-2]
    def _pseudo_next(self):
        '''Helper function for __next__. There are stored values
        on deck, so next is simulated rather than called.'''
        self.pos += 1
        return self.deq[self.pos - 1]
    def __iter__(self):
        return self
    def __next__(self):
        '''Analogous to __next__ associated with a call to iter.'''
        self.canditto = True
        return (reiter._pseudo_next,
                reiter._true_next)[
                not(self.pos < -1)](self)
    def __init__(self, iterator, memory_size=1):
        '''The iterator argument must be an iterator (could be
        iter(range(1)). The memory_size argument specifies the
        number of items to remember; expect strange behavior if
        this value is not a positive int.'''
        self._init_part_1(iterator, memory_size)
        self._true_next()
        self.canditto = False
    def ditto(self):
        '''Returns the most recent value returned by next or
        ditto. If seek is successful, subsequent calls to ditto
        have no effect, until next is again called.'''
        if self.canditto:
            return self.deq[self.pos - 1]
    def hist(self):
        '''Returns a tuple containing all of the values in the
        reiter-s memory, up to the current position.'''
        return tuple(self.deq)[:self.pos]
    def _retreat(self, n=1):
        '''Helper function for seek. Used when seek-s offset is
        negative.'''
        h = self.hist() # TO DO: a more efficient way to get length of history
        n = min(n, len(h)) # don't go back before history
        while n and (h[-n] is reiter.pre):
            n -= 1 # intend to go back as far as possible
        if not n:
            return 0 # n == 0
        self.pos -= n
        self.canditto = False
        return -n
    def _advance(self, n=1):
        '''Helper function for seek. Used when seek-s offset is
        positive.'''
        m = 0
        while n:
            if next(self) == reiter.post:
                self.canditto = False
                return m
            m += 1;   n -= 1
        return m
    def read(self):
        '''Alias for next. Analogous to the same-named method of
        a file object.'''
        return next(self)
    def seek(self, offset=0):
        '''Analogous to the same-named method for file objects.
        However, the conceptual 'from-what' parameter is always
        set to 'current position.' Returns the new position,
        relative to the initial position. If the offset argument
        would require more history than available, seek goes
        back as far as possible, which mean no change in the
        reiter object. If offset would require more values from
        the iterator than required, seek-ing stops just after
        the iterator is exhausted and the corresponding relative
        position is returned.'''
        return (self._advance, self._retreat)[offset < 0](abs(offset))
    def peek(self):
        '''Returns the next item, which will be a reiter.post
        object if the the reiter is exhausted, without advancing
        the reiter. Allows looking ahead one step. The oldest
        item in history may be sacrificed.'''
        item = next(self, reiter.post);   self.seek(-1)
        return item
    def index(self, test): # tag: skip search
        '''STATUS: untested!
        _advance-s reiter object to the point just before the
        next item to pass the test. Then, attempts to restore
        the position to its initial state. Returns the final
        position, relative to the initial position.
        
        STATUS: NEEDS WORK---RETURN VALUE DOES NOT GIVE PROPER
        INFORMATION
        
        '''
        assert 1 < 0, 'untested method'
        n = 0
        while (self.peek != reiter.post) and not test(self.peek):
            next(self);   n += 1
        return n - self._retreat(n)
    def asiter(self):
        '''Returns an iterator of the remaining items. Can be
        thought of as a dumbed down version of reiter.'''
        return chain(members(self.deq, range(self.pos, (0, -1)[self.deq[-1] is reiter.post])),
                self.iterator)
    def _state(self):
        '''Returns the important state variables as a dict.
        Intended for use during testing and debugging.'''
        return {'canditto': self.canditto, 'deq': self.deq, 'pos': self.pos }

def zipself(iterable, offset=None):
    '''Returns an iterator that produces (iterable[0],
    iterable[1]), (iterable[1], iterable[2]),... FUTURE: allow
    for offsets other than 1'''
    return fullgroups(rest(iter_double(iterable)))

def memo(iterator): ###
    '''STATUS: NOT BEHAVING AS EXPECTED: SEEMS TO RETURNING A
    GENERATOR RATHER THAN A FUNCTION. Returns a function of a
    nonnegative int which, in turn, returns the iterator's n-th
    item. Storage requirement: O(n). Intended for indefinite
    iterators---does not handle StopIteration exception.'''
    store = list()
    def inner(n):
        printerr('memo: inner:')
        while len(store) < (n + 1):
            store.append(next(iterator))
        return store[n]
    return inner

def find(value, iterable):
    '''Returns a map of indices, where each index locates the
    occurrence of value in iterable. It is possible that the map
    is empty, in the case where value does not occur.'''
    return map(first, filter(lambda tpl: value == second(tpl),
        enumerate(iterable)))

def findfirst(value, iterable):
    '''Finds the first instance of value in iterable, if it
    exists. Returns the integer index if found, -1 if not
    found.'''
    return next(find(value, iterable), -1)

def findlast(value, iterable):
    '''Finds the last instance of value in iterable, if it
    exists. Returns the negative integer index if found, 0 if
    not found.'''
    i = findfirst(value, reversed(iterable))
    return -1 - (i if 0 <= i else -1)

def findfirstamong(values, iterable):
    return findfirst(True, map(partial(fnin, values), iterable))

def root(function, value, iterable):
    '''STATUS: UNTESTED. Returns a map of indices, where each
    index locates the position where the function returns value
    for input equal to the corresponding item from the iterable
    It is possible that the map is empty, in the case where
    value does not occur.'''
    return find(value, map(function, iterable))

def memoize(dictionary, function, debug=False):
    '''STATUS: IN PROGRESS. May need a function to create a
    function of *args, **kwargs given any function, first.
    Intended to be used with partial to bake in the
    dictionary memo and the function function. In cases where
    the domains of multiple functions are disjoint, they might
    share the same dictionary. Whether this is recommended is
    another matter.'''
    def inner(*args, **kwargs):
        a = (args, kwargs) 
        ra = repr(a)
        if debug:
            print(ra)
        if ra not in dictionary:
            dictionary.update({repr(ra): function(*a)})
        return dictionary[repr(ra)]
        #return function(*args, **kwargs)
    return inner

def mapself(iterable):
    return map(ident, iterable)

def flat(*args): #TAGS chain flatten
    '''yield-s contents of args in sequence. Unlike chain
    (itertools), flat accepts args that are not iterable, which
    it simply yield-s. Example:
    >>> a, b, c = (0, (1, 2)), 3, (4, 5, 6)
    >>> tuple(flat(a, b, c))
    (0, (1, 2), 3, 4, 5, 6)
    >>> tpl = a, b, c
    >>> print(*flat(*tpl))
    0 (1, 2) 3 4 5 6
    >>> print(*flat(*flat(*tpl)))
    0 1 2 3 4 5 6
    '''
    for items in args:
        for item in forceiter(items):
            yield item

def flatt(compound_iterable):
    '''Similar to flat, but takes a single, compound iterable.
    Processes inner iterables one at a time; similarly for the
    items of the inner iterables.
            >>> tuple(flatt(map(
            ...     towords, 'line 1\nline 2\nline 3'.split('\n'))))
            ('line', '1', 'line', '2', 'line', '3')
    '''
    for iterable in compound_iterable:
        for item in iterable:
            yield item

def passover(*args, **kwargs):
    '''Can be used to pass over the members of an iterator, thus
    removing them. Example:
    .
            >>> it=iter(range(9));   passover(*quota(it, 5));   print(*it)
            5 6 7 8
    .
    See also: waste
    '''
    pass

def waste(iterable): ### tags: next
    '''Intended to exhaust all of the items in the iterable
    argument, in order to produce side effects, if any. Could do
    waste(quota(iterable, 3)) to advance iterable by 3 items.
    Another example:
    .
            >>> nul = waste(map(lambda x: print(x, end=' '), range(9)))
            0 1 2 3 4 5 6 7 8 >>>
            >>> it=iter(range(9));   nul = waste(quota(it, 5));   print(*it)
            5 6 7 8
    .
    HISTORY: 2018-03-17: modified to return iterator
    '''
    passover(*iterable)
    return iterable

def unchain(lengths, iterable): # tags: flat flatten
    '''Inverse of itertools.chain. The arguments are two
    iterables. The members of the first argument are int-s,
    each of which specifies the length of adjacent, disjoint
    subsequences of iterable. The unchain function yield-s one
    duple at a time, where the first item is the length of the
    iterator, and the second item is the iterator itself (c.f.
    enumerate).
    
    In the first example below, iterable yield-s int-s 0 through
    9 (inclusive), and lengths yield-s 1 through 4 (inclusive).
    In the second example, iterable yield-s 0 through 4
    (inclusive), and lengths yield-s 0 through 4 (inclusive);
    the iterator runs out of values before the number indicated
    by lengths:
    >>> for link in unchain(range(1, 5), range(10)):
    ...     print(*link[1])
    ...
    0
    1 2
    3 4 5
    6 7 8 9
    >>> for length, iterator in unchain(range(5), range(5)):
    ...     print('*', *iterator)
    ...
    *
    * 0
    * 1 2
    * 3 4
    *
    '''
    outer = iter(iterable)
    for length in lengths:
        assert isinstance(length, int)
        inner = quota(outer, length)
        yield length, inner
        waste(inner);   '''Re: waste(inner): Since all the
        inner-s are attached to the same outer, we need to
        advance through any remaining items in each inner before
        yield-ing the next one.'''

def unchainasreiters(iterator, lengths):
    '''Similar to unchain, but yield-s reiter-s rather than
    iterators. Storage requirement: O(n).'''
    for size, items in unchain(iterator, lengths):
        yield reiter(items, size)

def skip(iterator, n=1): ### tags: next
    '''Advances iterator *IN PLACE* n positions. Returns
    iterator. HISTORY: 2018-04-10: modified to return iterator.'''
    while (0 < n) and (next(iterator, NoMore) != NoMore):
        n -= 1
    return iterator

def takerest(iterable):
    return tuple(iterable)

def take(iterable, n=1): ### tags: next
    '''Takes as many items as are available from iterable, up to
    n, if n is nonnegative otherwise takes all items; returns
    items as a tuple.'''
    return tuple(quota(iterable, n))

def nextafter(iterator, n=0):
    '''Advances iterator *IN PLACE* n +1 items; returns n-th
    item, where n=0 indicates the next item prior to
    advancement.'''
    skip(iterator, n);   return first(take(iterator))

def skim(iterable, criterion=alwaysTrue, rejects=deque()): ###
    '''With analogy to skim-ming cream from separated milk,
    yield initial items in the (possibly sorted---e.g., cream on
    top) iterator that pass test (bool-ean function of one
    variable); append-s first reject (item not passing test) to
    rejects; then returns.'''
    for item in iterable:
        if not criterion(item):
            rejects.append(item);   return
        yield item

def draw(iterator, test, n=0): ### tags: get select next
    '''By analogy to DRAWing from a deck of cards, takes item-s
    (cards) from iterator until test(item) fails (unwanted
    card).  Returns a tripple containing: a tuple of the most
    recent n (or all, iff n == 0) items passing the test (all
    the cards you wanted), a singleton (tuple) containing the
    first reject (bad card), and the iterator itself (remaining
    cards). It will then be posible to reconstruct the iterator
    to its original state, or to produce an iterator that has
    all of the remaining items.  Example:
    >>> it=iter(range(9))
    >>> result=draw(it, lambda x: x < 4)
    >>> print(result)
    ((0, 1, 2, 3), (4,), <range_iterator object at 0x022A81A0>)
    >>> print(result[0])
    (0, 1, 2, 3)
    >>> print(*chain(*result))
    0 1 2 3 4 5 6 7 8
    >>> it=iter(range(9))
    >>> result=draw(it, lambda x: x < 4)
    >>> print(result)
    ((0, 1, 2, 3), (4,), <range_iterator object at 0x022A8CC8>)
    >>> print(*chain(*result[1:]))
    4 5 6 7 8
    '''
    assert isinstance(n, int), 'Third argument must be int.'
    d, reject = deque(), []
    for item in skim(iterator, test, reject):
        d = swab(append(d, item), n)
    return tuple(d), tuple(reject), iterator

def advanced(iterator, n=1):
    '''Pops *IN PLACE* n (optional arg) items from the iterator
    argument, provided that the iterator is not exhausted in the
    process. Exhausts the iterator if fewer than n items remain.
    Returns the iterator. Example:
    .
            >>> it=iter(range(9));   nul = advanced(it, 5);   print(*it)
            5 6 7 8
    .
    '''
    return waste(quota(iterator, n))

def advanceto(iterator, key, head=float('-inf'), tail=float('inf')): # tags: next
    '''Advances iterator *IN PLACE* past key. The modified
    iterator is not intended to be useful after a call to
    advance to; rather, it is anticipated that the returned
    iterator will provide utility. The iterable argument
    produces tuples in strictly ascending order based on their
    initial members (e.g., iter((0, 'spam'), (1, 42))).  Expect
    strange results if initial arguments repeat, i.e., if the order
    is not strictly ascending. These initial members i (not
    necessarily int-s) are copared using i <= key. The advanceto
    function runs through iterable until a value greater than
    that indicated by key is found or until iterable is
    exhausted (whichever comes first).
        The iterable argument could represent a piecewise linear
    function, and the key could represent a desired "x" value at
    which to read or interpolate a value from the function.
        Returns an iterator where key is between the first two
    items (may be equal to the first item, and is strictly less
    than the second item).
        In order to ensure this for all cases, in particular
    when key < i for all i or key > i for all i, a head and tail
    are prepended and appended to the iterator in an internal
    process; tail will be the chain-ed to the end of the
    returned iterator.
        Whether head is chained to the beginning is
    dependent upon the arguments. No tail will be appended if
    the corresponding argument is None; similarly for head.
    These are singleton tuples having members specified by the
    head and tail arguments.
        ASSUMPTION: head < i for all i and i < tail for all i.
    Originally intended for key to be either int or float, and
    that the items produced by iterable also have an int or
    float as the first member. C.f.  MS Excel VLOOKUP.
    >>> print(*advanceto(enumerate('ABC'), -99))
    (-inf,) (0, 'A') (1, 'B') (2, 'C') (inf,)
    >>> print(*advanceto(enumerate('ABC'), -.001))
    (-inf,) (0, 'A') (1, 'B') (2, 'C') (inf,)
    >>> print(*advanceto(enumerate('ABC'), 0))
    (0, 'A') (1, 'B') (2, 'C') (inf,)
    >>> print(*advanceto(enumerate('ABC'), 1.2))
    (1, 'B') (2, 'C') (inf,)
    >>> print(*advanceto(enumerate('ABC'), 2.5))
    (2, 'C') (inf,)
    '''
    def cmp(x):
        if x is head:
            return True
        if x is tail:
            return False
        return x <= key
    # the expression (((head,),), ())[head is None]
    # conditionally provides a head element for ri
    ri = reiter(chain(
            (((head,),), ())[head is None], iterator,
            (((tail,),), ())[tail is None]
        ), 2)
    drawn = draw(genapply(ri, first), cmp, 1)
    ri.seek(-2)
    return ri.asiter()

def sections(iterator, match=alwaysTrue, assess=constant(-1)):
    '''Modifies iterator *IN PLACE*. yield-s iterators. Each of
    the yield-ed iterators, in turn, produces items from the
    iterator (arg 1). By analogy with a document, the iterator
    is conceived of as having several sections. The first item
    of the iterator belongs to the first section. Whether each
    item belongs to the current or next section is determined
    via the match function, a function of head and the current
    item, and which returns a boolean value indicating whether
    the current item belons to the current section (True: "this"
    section; False: "next" section). Alternatively, the number
    of items in each section may be assessed via assess, a
    function of head.  Specification of both match and head may
    lead to strange results.  Examples:
    >>> for section in sections(iter(range(9)), match=lambda x, y: y - x < 4):
    ...     for item in section:
    ...         print('', item, end='')
    ...     print(' /', end='')
     0 1 2 3 / 4 5 6 7 / 8 /
    >>> for section in sections(iter(range(9)), assess=constant(2)):
    ...     for item in section:
    ...         print('', item, end='')
    ...     print(' /', end='')
     0 1 / 2 3 / 4 5 / 6 7 / 8 /
    >>> for section in sections(iter((1, 42, 3, 1, 2, 5, 0)), assess=lambda s: 1 + int(s)):
    ...     for item in section:
    ...         print('', item, end='')
    ...     print(' /', end='')
     1 42 / 3 1 2 5 / 0 /
    '''
    fore = []
    while True:
        head = fore.pop() if fore else next(iterator, NoMore)
        if head == NoMore:
            break
        yield chain([head], quota(iterator, n=assess(head) - 1,
                criterion=partial(match, head), forerunner=fore))

def sectionstagged(sects, key):
    for sect in sects:
        head, it = peek(sect)
        yield key(head), it


def filtermatch(subscriptable, iterators, keys):
    '''Given a subscriptable object (a control sequence) whose
    members are keys of interest, yield-s tuple-s containing the
    corresponding items from iterators (must be iterators, not
    merely iterable, for intended funciton), provided that the
    corresponding items are produced from *all* iterators as
    well as by the control sequence, *in the same order* as the
    control sequence. Whether items of iterators correspond to
    items of the control sequence is determined by the
    corresponding key function, taken from keys. It is expected
    that iterators and keys are of the same length. Example:
            >>> dates = 'July 3', 'July 4', 'Jul 5'
            >>> predicted = ('July 3', 'hot'), ('July 4', 'hot')
            >>> actual = ('July 4', 'cool'), ('July 5', 'warm')
            >>> for item in filtermatch(dates, (iter(predicted),
            ...         iter(actual)), (first,)*2):
            ...     print(*item)
            ...
            ('July 4', 'hot') ('July 4', 'cool')
            >>> # 'July 4' is the only key common to dates,
            >>> # predicted, and acutal.
    HISTORY: 2018-06-22 key variably in outer loop changed to
    KEY to deconflate with key.
    '''
    #printerr('filtermatch: subscriptable:', subscriptable)
    for KEY in subscriptable: # go through every key of interest
        printerr('filtermatch: KEY:', KEY)
        advanced_iterators, interesting_keys = [], []
        #count = 0 #DEBUG
        for iterator, key in zip(iterators, keys):
            #printerr('filtermatch: inner-loop-0: count:', count)
            #count += 1 #DEBUG
            '''Advance each member of iterators to the next
            interesting item.'''
            next_item, advanced_iterator = \
                    peek(filteruntil(
                            lambda x: key(x) in subscriptable, iterator))
            printerr('filtermatch: next_item:', next_item)
            if next_item is NoMore:
                return
            interesting_keys.append(key(next_item))
            advanced_iterators.append(advanced_iterator)
        most_advanced = subscriptable[
                findmax(interesting_keys, subscriptable)]
        final_advanced_iterators = []
        #printerr('filtermatch: interesting_keys:', interesting_keys)
        for iterator, key in zip(advanced_iterators, keys):
            '''Advance other iterators to the most advanced
            interesting item, skipping over unmatched items.'''
            printerr('filtermatch (second inner loop):')
            next_item, advanced_iterator = \
                    peek(filteruntil(
                            lambda x: key(x) == most_advanced, iterator))
            printerr('filtermatch (second inner loop): next_item:', next_item)
            if next_item is NoMore:
                return
            final_advanced_iterators.append(advanced_iterator)
        #printerr('filtermatch:', final_advanced_iterators)
        yield tuple(map(next, final_advanced_iterators))

def restricted(iterable, interval, tail=float('inf')): # tags: band domain
    '''May modify iterable *IN PLACE*, particularly if iterable
    is an iterator.  The iterable argument produces values that
    are consistent with the iterable argument of advanceto.
    Returns a duple that contains values that completely cover
    the interval specivied by the argument of that name. Can be
    used in a step in an interpolation process: restricted
    may be made to return the necessary tuples (e.g., ordered
    pairs). The return may also be applied to recycle the values
    from the initial iterable. See also restricted domain
    function. Example:
    >>> pairs = enumerate(map(lambda x: x*x, range(9)))
    >>> nextfew, rest = restricted(pairs, (-99, -99))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((-inf,), (0, 0))
    >>> nextfew, rest = restricted(chain(nextfew, rest), (2.5, 2.5))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((2, 4), (3, 9))
    >>> nextfew, rest = restricted(chain(nextfew, rest), (4.7, 4.7))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((4, 16), (5, 25))
    >>> nextfew, rest = restricted(chain(nextfew, rest), (4.7, 99))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (inf,))
    >>> nextfew, rest = restricted(chain(nextfew, rest), (5, 99))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((5, 25), (6, 36), (7, 49), (8, 64), (inf,))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((5, 25), (6, 36), (7, 49), (8, 64), (inf,))
    >>> nextfew, rest = restricted(chain(nextfew, rest), (5, 999))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((5, 25), (6, 36), (7, 49), (8, 64), (inf,))
    >>> nextfew, rest = restricted(chain(nextfew, rest), (99, 999))
    >>> nextfew # ... use elsewhere to interpolate a value ...
    ((8, 64), (inf,))
    '''
    drawn = draw(advanceto(iter(iterable), first(interval),
        tail=tail), lambda
        item: first(item) <= second(interval))
    return tuple(chain(*drawn[:2])), drawn[-1]

def samples(iterator, intervals, tail=float('inf')):
    '''yield-s "samples" from a "signal." The iterator argument
    produces items consistent with advanceto, and intervals is
    an iterable that produces items consistent with the
    same-named argument of restricted. The samples function
    yield-s a tuple containing the interval and associated
    sample. Depending on the arguments, samples yield-ed may
    include a tail (see restrict and advanceto). No
    interpollation is done to achieve a sample that precisely
    fits a corresponding interval. Rather, enough informaiton is
    produced in the associated sample to enable such
    interpolation'''
    nextfew, rest = (), iterator
    for i, interval in enumerate(intervals):
        nextfew, rest = restricted(chain(nextfew, rest), interval,
                tail=(tail, None)[bool(i)]) # append tail on first call only
        yield interval, nextfew

def tightsample_lin(interval, sample, index=0): # TO DO: SET DEFAULT INTERPOLATION FUNCTION: ASSUME DATA ARE tuple-S OF NUMERIC VALUES
    '''interval: duple of scalar numeric values. sample: an
    iterable of tuples; each tuple has the same number of scalar
    numeric values. conceptually, each item in sample forms a
    node in a mulidimensional piecewise linear curve. Example:
    >>> tightsample_lin((.5, 1.5), ((0,), (1,), (2,)))
    ((0.5,), (1,), (1.5,))   
    >>> tightsample_lin((.5, 1.5), ((0, 0), (1, 10), (2, 20)))
    ((0.5, 5.0), (1, 10), (1.5, 15.0))

        '''
    s = tuple(sample)
    inp = partial(interp_lin, index=index)
    return    astuple(inp(s[:2] , interval[ 0])) \
            + sample[1:-1] \
            + astuple(inp(s[-2:], interval[-1]))

def slide(appendable, iterator, n=1):
    '''By analogy with the wire of an abacus, n items "slide"
    from the iterator and are appended *IN PLACE* to appendable.
    Returns appendable.'''
    appendable += quota(iterator, n)
    return appendable
        
def running(iterable, n=2): #.# tag: lag
    '''Provided that iterable produces at least n items, yield-s
    entire contents of iterable, one window at a time. Each
    window is n items wide.  Can be applied to the computation
    of running averages. Example:
            >>> print(*running(iter(range(4))))
            (0, 1) (1, 2) (2, 3)
    HISTORY: 2018-01-13: revised to avoid using next and to
    handle iterators producing n or fewer items, and to yield
    tuple rather than list. 2018-02-20: revised to create
    iterator it from iterable.'''
    it = iter(iterable)
    d = deque(take(it, n))
    if len(d) < n:
        return # iterator exhausted before desired length reached
    yield tuple(d)
    for item in it:
        yield tuple(shiftinv(d, item))

'''
def nextchunk # use nmore #TAGS next
'''

def chunks(iterator, sizes):
    '''yield-s tuples of items in interator according to the
    chunk sizes given by the iterable sizes. Exhausts when
    either iterator or sizes are exhausted.'''
    for size in sizes:
        mo = nmore(iterator, size)
        if mo:
            yield mo
        else:
            return

def nextastuple(iterator):
    '''Returns the next item of iterator, enclosed in a tuple.
    If the iterator is exhauseted, the tuple is empty. Can be
    used in combination with a test of len of the return value.
    Example: see nextgroup.'''
    item = next(iterator, NoMore)
    return () if item is NoMore else (item,)

def nextgroup(iterator, n=2):
    '''Returns a tuple which contains n items retrieved from
    iterator, provided that n items are produced. If the
    iterator is exhausted in the process, the tuple will contain
    the corresponding number of items, possibly zero.'''
    return tuple(quotan(iterator, n))

def nextgroupm(iterator, n=2):
    '''Returns a map of the next n items from iterator.'''
    return quota(iterator, n)

def peek(iterator, default=NoMore):
    '''Advances iterator *IN PLACE*. Returns a duple containing
    the next item (or default) and another iterator that
    produces the item, followed by the remaining items of the
    iterator.'''
    item = next(iterator, default)
    return item, chain((item,), iterator)

def groupsm(iterator, n=2):
    '''yield-s maps of n items from the iterator. Strange
    behavior may result if the maps are not exhausted in turn.
    Exmample (see also groupsmm):
for item in groupsm(iter(range(14)), 6):
    print(*item)
            0 1 2 3 4 5
            6 7 8 9 10 11
            12 13
    '''
    while True:
        x, group = peek(nextgroupm(iterator, n))
        if x is NoMore:
            return
        yield group

def groupsmm(iterator, groupsizes=()): #TAGS array hierarchy
    '''yield-s maps of maps of ... maps of items. The number of
    levels is len(n). The elements of groupsizes (int-s)
    determine the maximum group size (actual group size also
    depends upon the nuber of items produced by iterator).
    Originally intended to be applied to an iteration through an
    array, and to facilitate different procedures at different
    levels (e.g., element, column, row).  Strange behavior may
    result if the maps are not exhausted in turn, or if elements
    of groupsizes are not increasing.  Example:
    for item in groupsmm(iter(range(48)), (8, 12, 24)):
        print('\nnewlayer', end='')
        for thing in item:
            print('\nnewrow', end='')
            for obj in thing:
                print('\nnewline', end='')
                print('', *obj, end='')
    
                newlayer
                newrow
                newline 0 1 2 3 4 5 6 7 8 9
                newline 10 11
                newrow
                newline 12 13 14 15 16 17 18 19 20 21
                newline 22 23
                newlayer
                newrow
                newline 24 25 26 27 28 29 30 31 32 33
                newline 34 35
                newrow
                newline 36 37 38 39 40 41 42 43 44 45
                newline 46 47>>>
    '''
    if not groupsizes:
        return
    for thing in groupsm(iterator, groupsizes[-1]):
        yield thing if len(groupsizes) < 2 else groupsmm(thing, groupsizes[:-1])

'''TESTS

    it = iter(range(42))
    for item in groupsm(it, 6):
        print()
        for thing in groupsm(item, 2):
            print(*thing)
    
    it = iter(range(42))
    for item in foo(it):
        print(*item)
    
    it = iter(range(42))
    for item in foo(it, (6,)):
        print(*item, sep=' :')
    
    g1, g2 = groupsm(it, 6)
    print(*g1)
    
    it = iter(range(42))
    print(*nextgroupm(it, 6))
    
    it = iter(range(42))
    print(*nextgroupm(nextgroupm(it, 5), 3))
    
    def foo(iterator, n=6):
        for nextgroupm(nextgroupm(it, 6)):
            print(type(grp))
            x, grp1 = peek(grp)
            if x is NoMore:
                return
            yield grp1
    
    it = iter(range(42))
        for item in foo(it):
        pass
    
    
    it = iter(range(42))
    for item in foo(it):
        print(item)
        for thing in foo(item, 2):
            print(';', *thing)
            print()

'''

def groups(iterator, n=2):
    '''Yields items in iterator, grouped as tuples of length n.
    The last group will be partial, possibly empty, according to
    n and the available items in iterator.'''
    while True:
        g = nextgroup(iterator, n=n)
        yield g
        if len(g) < n:
            break

def fullgroups(iterator, n=2):
    '''Returns a generator that produces n items at a time from
    iterator. Wastes the last 1 to n - 1 items, if iterator does
    not produce a multiple of n items.'''
    for g in groups(iterator, n):
        if len(g) < n:
            break
        yield g

def chainextendleft(iterator, n=1, value=None):
    return chain((value,) * n, iterator)

def cumulative(iterator=None, history=0, persistent=False, function=lambda n, n0: n0):
    '''Returns a generator that yield-s values from a sequence
    defined by the arguments.  The first few values of the
    generated sequence are determined by history.  history
    should be a single value or a tuple of values.  The number
    of values stored depends on persistent: store only the
    number of values represented by the history (1 or
    len(history)) argument if not persistent; store all values
    if persistent.  for each item in the sequence beyond those
    specified by history, the items are computed by function, a
    function of two variables: arg 0 is a deque containing the
    previous few values (the number of which is determined by
    persistent and or history) and arg 1 is next(iterator).
    Alternatively, function may be a str that is the right hand
    side of the lambda expression (lambda n, n0:).  Examples
    (see also: cumulative_sum, cumulative_product):
    print(*quota(skip(cumulative()), 9)) # natural numbers
    print(*quota(cumulative(indefinite(2), history=1, function=lambda n, n0: n[-1] + n0), 9))
            # triangular numbers
    print(*quota(cumulative(indefinite(2), history=1, function='n[-1] + n0'), 9))
            # triangular numbers
    print(*quota( skip(cumulative(function='n[-1] + n0 * n0')) , 9))
            # sum of squares 
    print(*quota(skip(cumulative(skip(indefinite()), function='n[-1] + n0 ** 3')), 9))
            # sum of cubes
    print(*quota(cumulative(steady(None), history=(0, 1), function='n[-2] + n[-1]'), 9))
            # Fibonacci numbers # TO DO: why doesn't # function='sum(n[-2:])' work?
    print(*quota(cumulative(indefinite(2), history=(1, 1), function='n[-1] * n0'), 9))
            # factorials
    print(*quota(
        cumulative(indefinite(2), history=(0, 1), persistent=True,
            function='n[-1] - n0 if (n0 < n[-1]) and (n[-1] - n0) not in n else n[-1] + n0'),
        9))
            # Recamans_sequence
    '''
    if isinstance(function, str):
        function = eval('lambda n, n0:' + function)
    if not iterator:
        iterator = skip(indefinite())
    history = deque(tuplefy(history))
    update = deque.append if persistent else shiftinv
    for item in history:
        yield item
    for item in iterator:
        update(history, function(history, item))
        yield history[-1]

def cumulative_product(iterator):
    return skip(cumulative(iterator, history=1, function='n[-1] * n0'))

def cumulative_sum(iterator):
    return skip(cumulative(iterator, function='n[-1] + n0'))

def accumulate(iterable, initializer=0, function=lambda x, y: x + y): ###
    '''Special case of reduce. Returns a tuple, each element of
    which is the result of evaluating function with an
    initial argument of the most recently appended item of the
    result and with a secondary argument equal to the current
    element of iterable. E.g.  accumulate(range(8), 1, lambda x,
    y: x * (y + 1)) returns a sequence of factorials beginning
    with 1 factorial.
    HISTORY: 2018-02-05: now returns tuple (was list)
    TO DO: rework in terms of cumulative.'''
    from functools import reduce
    return tuple(reduce(lambda x, y: x + [function(x[-1], y)], iterable, [initializer])[1:])

'''
def classcount #DEPRECATED use tally(classify(iterable))
instead, where classify is a classification function
'''
def classcount(things, keys=(False, True, None), classify=bool): ###
    '''Returns a dict with a key for each bin. HISTORY
    2018-11-02: keys was formerly called bins. classify was
    formerly lambda x: x != 0'''
    count = dict(zip(keys, map(lambda x: list((0,)), steady(None))))
    for thing in things:
        count[classify(thing)][0] += 1
    return dict(map(lambda item: (item[0], item[1][0]), count.items()))

def tally(iterable): #TAGS count
    tal = dict()
    for item in iterable:
        if item in tal:
            tal[item] += 1
        else:
            tal.update({item : 1})
    return tal

def duplicates(iterable):
    '''Returns the set of items duplicated among the items
    produced by iterable.'''
    dups, orig = set(), set()
    for item in iterable:
        (orig, dups)[item in orig].update((item,))
    return dups

def lastitem(iterable): ###
    from functools import reduce
    return reduce(lambda x, y: y, iterable)

def anycomp(comp, thing, iterable): ###
    '''Returns a bool value indicating whether any items in iterable return True for comp(thing, item)'''
    from functools import partial
    return any(map(partial(comp, thing), iterable))
