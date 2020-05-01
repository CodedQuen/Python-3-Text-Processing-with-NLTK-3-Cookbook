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
# 1. INDEPENDENT GENERATORS
# 2. FUNCTIONS OF GENERATORS


# INDEPENDENT GENERATORS

def train(compound_iterable=(())): ### #TAGS chain
    '''Similar to itertools::chain, but takes a single argument,
    which is an iterable of iterables. Unlike chain, the
    argument may produce an infinite iterables, and any of the
    iterables may produce infinite items. Example:
            >>> t = train(steady((0, 1)))
            >>> next(t)
            0
            >>> next(t)
            1
            >>> next(t)
            0
    '''
    for iterable in compound_iterable:
        for item in iterable:
            yield item

def split(iterator, key=ident):
    assert False, 'PLACEHOLDER'
    for key in everykey(fd['r'][0]):
        with openw(dirout + key) as fo:
            printerr('all-meas.py split: key:', key)
            for line in rewind(fd['r'][0]):
                k = first(towords(line))
                if k == key:
                    fo.write(line)

def indefinite(n=0): ### #TAGS: infinite natural numbers
    while True:
        yield n
        n += 1

def randoms(): ###
    '''yield-s an indefinite quantiy of radom floats by repeated
    calls to random.'''
    from random import random
    while True:
        yield random()

def irandoms(n=2): #.#
    '''yield-s random values selected from the first n
    nonnegative integers.'''
    for r in randoms():
        yield int(n * r)

def cycle(period=1):
    assert isint(period), 'period must be int.'
    assert 0 < period, 'period must be positive.'
    while True:
        for i in range(period):
            yield i

def echoes(x, n=1): ### tags: repeat repetition copies duplicate replicate
    return map(constant(x), range(n))

def sequence(*args):
    '''sequence(gen1, gen2,...) returns the items of gen1, followed by the items
    of gen2. DEPRECATED: use chain from itertools.'''
    for gen in args:
        for item in gen:
            yield item

def iter_double(iterator): ###
    '''Yields for each item in iterator, yields two copies, in the pattern
    item0, item0, item1, item1, ...'''
    for item in iterator:
        yield item
        yield item

####

def memo(thing):
    while True:
        yield thing

def nextorcurrent(gen, default=None, current=None, option=True):
    if option:
        return next(gen, default)
    return current

def asgen(x):
    for item in x:
        yield item

def decimate(gen, outof=1, keep=0):
    '''Receive items from generator gen. The items are assumed
    to arrive in ordered sets of cardinality outof. From each
    ordered set, yield only the keep-th item.'''
    #print('decimate:', 'keep:', keep)
    for i in range(keep): # initialize generator position
        next(gen)
    kk = cycle(outof)
    for item in gen:
        if not next(kk): # works because of initialization
            yield item


#def deinterlace(gen, rlen=1)
    #'''receive generator gen (sequences of rlen items) a sequence of items
#
    #synonymns: transpose, vectorize
#
    #item[0][0] item[] 1 B1 ... 
#
    #'''


def genbytefrom(f):
    '''"byte generator from [file]" yields bytes (as strings of length 1) from
    file f.'''
    while True:
        c = fread(f)
        if not c:
            return
        yield c

def genenumeratedbytes(f):
    '''Similar to enumerate, applied to a file. Yields duples containing file
    position followed by the character at that file position. Characters may
    vary depending on mode (e.g., 'r' vs. 'rb').'''
    f.seek(0)
    while True:
        t, c = f.tell(), fread(f)
        if not c:
            return
        yield t, c

#### counter Function, Helper, and Example Application

def carry(lst, ctr, i=0): ###
    '''Applies carry to list of integers lst. Valid values of each element of
    lst are determined by ctr, a list of generators.  Assumes carry condition
    has occured because digit i has rolled over from maximum to minimum (e.g.,
    as the minute hand of the clock increments from 59 to 0). Example:
    carry([0,9,1],ctr,0), where ctr is consistent with a base-10 counter, should
    modify lst to [0,0,2]. Originally intended as a helper function for
    counter.'''
    j = i + 1
    if j >= len(lst):
        return
    if not lst[i]:
        lst[j] = next(ctr[j])
        carry(lst, ctr, i=j)

def counter(*limits):
    '''Generates lists of nonnegative integers in ascending
    order, in a manner simiar to an odometer, tape counter, or
    digital clock. The first member of each item generated is
    the "fastest changing."
    
    Examples:
        five_digit_odometer = counter((10,10,10,10,10))
        tape_counter = counter((10,10,10))
        clock_military = counter((10,6,10,6,24))
        # seconds, tens of seconds, minutes, tens of minutes, hours
    '''
    assert all(map(partial(argswap(isinstance), int), limits)), 'arguments must be int-s.'
    assert all(map(partial(argswap(greater), 0), limits)), 'each argument must be positive.'
    ctr = tuple(map(cycle, limits))
    cur = list(map(lambda x: x - 1, limits))
    while True:
        cur[0] = next(ctr[0])
        carry(cur, ctr)
        yield tuple(cur)

def gridindices(*m):
    '''Returns a map of integer tuples, each of which represents
    an array index of len(m) dimensions. The indices proceed in
    increasing order from zero, where the "faster" indices are
    first.  Example:
            >>> tuple(gridindices(3, 2)
            ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1))
    '''
    return quota(map(tuple, counter(*m)), product(*m))

def gridindicessquare(width, ndims=2):
    '''similar to gridindices; however, all dimensions are the
    same: the indices represent a square, cube, hypercube, etc.
    region.
            >>> tuple(gridindicessquare(3, 2))
            (
                (0, 0), (1, 0), (2, 0),
                (0, 1), (1, 1), (2, 1),
                (0, 2), (1, 2), (2, 2))
            >>> #CR AND SPACES ADDED FOR CLARITY
    '''
    return unstar(gridindices)((width,) * ndims)

def counterserialno(lst, rngs):
    '''STATUS: IN PROGRESS. returns a unique value corresponding to a value represented by a
    counter. TO DO: USE PLACE VALUE, DOT PRODUCT'''
    lst[0]+rngs[0]*lst[1]
    for item in enumerate(lst):
        val = 0
    for i in range(1,len(lst)):
        val = val + rngs[i]*lst[i-1]

def counterbijectivebase26():
    pass

def counterprint(tpl,rvs=False):
    # TO DO: refactor by applying list versin of format, fformat
    digs = []
    for item in tpl:
        digs.append(1+places(item))
    fmt = []
    for item in digs:
        fmt.append('{0:'+str(item)+'d}')
    if rvs:
        fmt.reverse()
    for item in counter(tpl):
        cpy = item
        if rvs:
            from copy import deepcopy
            cpy = deepcopy(item)
            cpy.reverse()
        print('A',1+item[2],sep='',end='') # jerryrig for special case
        for thing in enumerate(cpy):
            #print('thing:',thing,'format:',fmt[thing[0]],end=' ')
            print(fmt[thing[0]].format(1+thing[1]),end='')
            # adding 1 to thing[1] is a jerryrig for a special case
        print()
    print()

'''
def constant... #REMOVED (defined in maths.py)
'''

# FUNCTIONS OF GENERATORS
#
# The general aim of the initial development of these functions
# is concerned with the reading of sequential files into tokens.
# The structure of the file is considered to be alternating
# sequences of significant (i.e., data) and insignificant (i.e.,
# separator) bytes.

# Functions receiving generator and other parameters and returning a generator

def gengen(gentpl):
    '''Yields all of the items of the generators in the tuple of generators
    gentlp'''
    for gen in gentpl:
        for item in gen:
            yield item

def genfirst(gen): ###
    'Yield the first item in generator gen, if there is one.'
    for item in gen:
        yield item
        break

def rest(iterator): ###
    'Throw away first item, if there is one.'
    for item in iterator:
        break
    return iterator

def genlimit(gen, items=1): #.#
    '''Deprecated. use quotan.'''
    return quota(gen, items)


####

def genseqdupind_(gen):
    'helper function for genseqdupind'
    ndx = -1
    ndxx = []
    for item in genlag(gengen((asgen([None]), gen, asgen([None])))):
        ndxx.append(ndx)
        ndx = 1 + ndx
        if second(item) != first(item):
            yield tuple(ndxx)
            ndxx = []

def genseqdupind(gen):
    '''Generate Sequential Duplicate Indices. For each subsequence of elements
    of gen which compare equal, yield a tuple containing their indices. For
    example, if gen generates the sequence 1, 2, 2, 2, 2, 4, 4; the following
    sequence of tuples will be yielded: (0,), (1, 2, 3, 4), (5, 6).'''
    for item in genrest(genseqdupind_(gen)):
        yield item

def genseqdupmultiplicity(gen):
    '''Generate the multiplicity of each subsequence of elements of gen which
    compare equal.'''
    for item in genseqdupind(gen):
        yield len(item)

####




def gencopies(gen, n=2):
    '''"Duplicate items [from generator]" Returns an generator that yields
    multiple copies of each item pulled from a generator, as a tuple'''
    for item in gen:
        yield (item,) * n

def gensubst(gen, keep=alwaysTrue, sub=ident):
    '''Substitute. For each item in generator gen, apply function keep to
    determine whether to keep the item. Yield the item if kept. Otherwise,
    yield the return of the function sub.'''
    for item in gen:
        yield item if keep(item) else sub(item)

def wax(appendable, iterable): ###
    '''append-s *IN PLACE* appendable with one item from
    iterable, then yield-s the modified appendable. Originally
    intended to be applied to accumulate into a deque a limited
    number of characters from a file. Also originally intended
    that appendable will be occaisionaly reduced in size by an
    outside process before too many items accumulate. Example:
    >>> for item in wax([], iter(range(3))):
    ...     print(item)
    ...
    [0]
    [0, 1]
    [0, 1, 2]
    ''' 
    for item in iterable:
        appendable.append(item)
        yield appendable

def waxuntil(appendable, iterable, test): #.#
    '''Repeatedly appends appendable with items from iterable. 
    yield-s those items that pass the test. Example:
    >>> for item in waxuntil([], iter(range(1,9)), lambda x: x and x[-1] % 2):
    ...     print(item)
    ...
    [1]
    [1, 2, 3]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5, 6, 7]
    '''
    for item in wax(appendable, iterable):
        if test(item):
            yield item

genwax = wax #DEPRECATED use wax

def waxuntil(appendable, iterable, stop):
    while not stop(appendable):
        wax(appendable, iterable)
    return appendable

def genunwax(gen, test=alwaysFalse):
    '''Receive pop-pable items from generator gen. Yield conditionlaly pop-ped
    items based on applying function test to each item. Originally intended to
    process lists with trailing insignificant items (e.g., whitespace afer a
    word).'''
    for item in gen:
        if len(item):
            if test(item):
                item.pop()
        yield item

def genlunwax(gen, test=alwaysFalse):
    '''Receive popleft-able items from generator gen. yield
    possibly modified versions each item, according to function
    test.'''
    for item in gen:
        if len(item):
            if test(item):
                item.popleft()
        yield item

def genseq(gen, endex=alwaysneg1):
    '''Receive popleft-able items from generator gen; popleft a number of sub-
    items from the item in question. The number of items is indicated by endex,
    a funciton of the item in question that returns the index of of the first
    sub-item that is not to be popleft-ed. If index returns 0, no items are
    popped. Originally intended to be applied to a generator that accumulates
    into a single deque a limited number of characters from a file: the present
    function then removes atomic items from that deque, which atoms may consist
    of multiple subatomic items from the left side of the deque.  We purpose-
    fully don't import deque; that should already have been done by the caller;
    if not, we want to produce the corresponding error.'''
    for deq in gen:
        lsd = list(deq)
        n = endex(lsd)
        lst = lpopn(deq, endex(lsd))
        if len(lst):
            yield lst

def genatoms(gen, issubatom=isgraph, sep=' '):
    '''Receive subatomic items from generator gen. build and yield atoms made
    up of sequential subatomic items itentified by the boolean function
    issubatom. sequences of subatomic items are separated by items for which
    issubatom returns False. The object sep will be placed between sequences of
    subatomic items in an intermediate step.
    KNOWN ISSUES:
    appears to be slow when issubatom is other than default
    appears to want to build the entire sequence before yielding the first item.
    '''
    from collections import deque
    s = [] ##
    # the '##' comments reflect the contents of stack s after the corresponding
    # statement has been completed.
    s.append(lambda x: indexnice(x, sep)) #4# parameter for genseq
    s.append(lambda x: False if not len(x) else not issubatom(first(x))) #43#
    s.append(lambda x: False if len(x) < 2 else eq(x) and not issubatom(second(x)))#432#
    s.append(lambda x: sep) #4321# # parameter for wax
    t = gensubst(gen, keep=issubatom, sub=s.pop()) #432#
    t = wax(deque(), t) #432#
    t = genunwax(t, s.pop()) #43#
    t = genlunwax(t, s.pop()) #4#
    #return genseq(t, s.pop()) ##
    for item in genseq(t, s.pop()): ##
        yield item
    '''
    # THE FOLLOWING VERSION OF genatoms is EQUIVALENT
    def genatoms(f, issubatom=isgraph, sep=' '):
    # THE ILLEGAL INDENT ABOVE IS ADDED FOR AESTHETICS
    from collections import deque
    fsub = lambda x: sep                                                           #1#
    waxtest = lambda x: False if len(x) < 2 else eq(x) and not issubatom(second(x)) #2#
    unwaxtest = lambda x: False if not len(x) else not issubatom(first(x))          #3#
    ndex = lambda x: indexnice(x, sep)                                             #4#
    gen = gensubst(genbytefrom(f), keep=issubatom, sub=fsub) #1#
    gen = wax(deque(), gen)
    gen = genunwax(gen, waxtest)                            #2#
    gen = genlunwax(gen, unwaxtest)                         #3#
    return genseq(gen, ndex)                                #4#
    '''

def genfromseqfile(f, issubatom=isgraph, sep=' '):
    '''yields contents of file f, one atom at a time, where an atom consists of
    a list of subatomic items defined by the boolean test function issubatom.
    Subatomic items for which issubatom returns False are considered
    separators; sequential separators are considered equivalent to a single
    separator, and separators are coverted to the item indicated by sep in an
    intermediate process.'''
    return genatoms(genbytefrom(f), issubatom=issubatom, sep=sep)

def genstrfromlststr(gen):
    '''"Generate strings from lists of strings." Receive lists of strings (one
    list at a time) from generator gen. For each list received, yield the
    concatenation of the strings contained.'''
    for j, lst in enumerate(gen):
        yield ''.join(lst)
    printerr('(STATUS)', 'genstrfromlststr:', 'items:', 1 + j)

def gengroups(gen, n=1):
    '''"Generate groups." Receive items from generator gen.
    Yield lists of n items.'''
    lst = []
    for item in gen:
        lst.append(item)
        if len(lst) == n:
            yield lst
            lst = []

def genclassmembers(gen, classify=ident):
    from collections import deque
    for d in wax(deque(), gen):
        if classify(first(d)) != classify(last(d)):
            yield lpopn(d, len(d) - 1) # list of subsequent items comparing equal
    # d should either be empty or contain only matching items.
    if len(d):
        yield list(d)

def genfloatfromstr(gen):
    '''"Generate floats from strings." Receive strings from generator gen.
    Yield floats. Strings for which the float function fails are converted to
    values equivalent to float('nan').'''
    return map(nicefloat, gen)

def nextall(iterators):
    return tuple(map(partial(argswap(next), NoMore), iterators))

def nextall_clipped(iterators):
    '''Similar to nextall, but returns a tuple of NoMore-s if
    any of the items of the return of nextall are NoMore-s. Cf.
    zip.'''
    nxt = nextall(iterators)
    return (NoMore,) * len(iterators) if \
        any(map(partial(equal, NoMore), nxt)) else nxt

def nextall_old(gens, defaults=kwarg_missing):
    '''HISTORY 2018-06-08: renamed w/ _old suffix to accomodate
    recoding '''
    if defaults is kwarg_missing:
        defaults = (end_of_iterator,) * len(gens)
    items = []
    for i, gen in enumerate(gens):
        items.append(next(gen, defaults[i]))
    if all(map(lambda x: equal(*x), zip(items, defaults))): # TO DO: refactor
        raise StopIteration
    return items

def genfuncvaluefromtpl(gens, fun=sum):
    '''"Generator of function values." Returns a generator of function values.
    The function fun is a function of several (positional) variables, which
    are populated from the tuple of values received from gen.
    Example:

    for s in genfuncvaluefromtpl(range(9),range(9)):
        print(s,sep=' ')

    will print the following to stdout
    0 2 4 6 8 10 12 14 16
    '''
    return map(fun, zip(*gens))

def edges(iterator): #TAGS xor exclusive or difference
    '''returns a map of indices of pairs of items from the
    iterator argument where the members of the pairs are
    unequal. The first pair has an index of zero. The last item
    of the iterator is considered unequal to a hypothetical
    element that comes after the last item of the iterator.
            >>> tuple(edges((2,3,3,4,4,5)))
            (0, 2, 4, 5)
            >>> tuple(edges((42,)))
            (0,)
            >>> tuple(edges(()))
            ()
    '''
    return map(first, filter(
        lambda tpl: unstar(un(equal))(second(tpl)),
        enumerate(running(chain(iterator, echoes(object(), 2))))))

def genlag(iterable, n=2): # tag: running
    '''Deprecated. Use running.'''
    return running(iterable, n=2)

def genlagbyfn(gen, fn=lambda x, y: True):
    '''Similar to genlag, but applies the function fn to determine whether to
    include the next item in the group of items presently under construction.
    In the default fn, x is the present group and y is the candidate item
    under consideration. A group is yielded when fn returns False.'''
    from collections import deque
    d = deque([])
    items = 0
    for item in gen:
        d.append(item)
        items = items + 1
        break
    if not items:
        yield list(d)
        return
    for item in gen:
        nxt = item
        if fn(tuple(d), nxt):
            d.append(nxt)
        else:
            yield list(d)
            d = deque([nxt])
    yield list(d)

def genlagapply(gen, lagparm=2, fn=ident):
    '''There is a tradition in Forth to solve the most difficult problem
    first; the other problems solve themselves.---paraphrasing Ting in eForth
    and Zen, 3rd. ed. See also genrunningweightedaverage.'''
    lagger = [genlagbyfn, genlag][type(lagparm)==type(1)]
    for item in genapply(lagger(gen, lagparm), fn):
        yield item

def genrunningweightedaverage(gen, w=(-1, 1)):
    'The default w=(-1, 1) produces backward differences.'
    for item in genlagapply( gen, len(w), lambda x: dot((x, w)) ):
        yield item

def genindex(gen, test):
    '''The function test is evaluated for each item yielded by generator gen.
    Returns a generator indices where fin returns True.'''
    return map(first, filter(second, enumerate(map(test, gen))))

def nextn(iterator, n=1):
    '''Advance generator n items: return n-th item beyond the
    current (item 0).'''
    assert isint(n) and 0 < n, 'n must be a positive int.'
    item = first(throughto(
        deque([(None, NoMore)]), enumerate1(quotan(iterator, n)), alwaysFalse))
    return second(item) if first(item) == n else NoMore

def genseptext(gen, groups, eol='\n'):
    '''Receive strings from generator gen. Yield the same strings prepended
    with the string pre, but yield eol immediately after a group of any of the
    sizes specified by the tuple groups has been yielded. STRANGE BEHAVIOR may
    occur if each positive integer in groups is not greater than the last.
    Originally intended to reformat very long lines of text for use in programs
    that are sensitive to line length, such as R and Fortran. HISTORY 2018-09-17 removed pre parameter; remap input to include pre-characters if desired.'''
    kk = list(map(cycle, groups))
    k  = list(map(next, kk))
    for st in gen:
        k  = list(map(next, kk))
        yield st
        for i in enumerate(k):
            if not second(i):
                yield eol # the end of a group has been reached.
                for j in enumerate(kk):
                    if first(j) >= first(i):
                        break # don't adjust the larger groups' counters
                    while next(second(j)):
                        pass # reset the smaller groups' counters
                break

def genlinesfromfile(f, strip=False, stripEOL=False):
    while True:
        ln = f.readline()
        #printerr(ln) #DEBUG
        if not ln:
            break
        if stripEOL:
            if last(ln) == '\n':
                ln = ln[:-1]
        yield [ln, ln.strip()][strip]

def genfindall(obj, sub, start=0): ###
    '''Generates all indices of subsequence sub in object obj.
    Tested on bytes and string objects.'''
    while start < len(obj):
        start = obj.find(sub, start)
        if start < 0:
            return
        yield start
        start = start + 1
