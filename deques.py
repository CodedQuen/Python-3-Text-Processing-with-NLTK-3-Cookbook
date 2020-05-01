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

def popleft(popleftable):
    '''If possible, popleft-s the argument *IN PLACE*. Returns
    the possibly modified argument, UNLIKE deque.popleft, which
    returns the popleft-ed item.'''
    assert popleftable.popleft
    return popleftable if not popleftable else (popleftable.popleft(), popleftable)[1]

def recent(iterator, n=1):
    '''Exhausts iterator. The lesser of n or the number of items
    available in the iterator are returned as a tuple.'''
    deq = thread(deque(), iterator, n)
    return second((waste(map(partial(shiftinv, deq), iterator)), deq))

def throughto(deq, iterator, stop): #.# tags: iterate lookup shiftin
    '''shiftin-s values as long as not stop---a function of
    deq---and the iterator is not exhausted. If iterator and
    stop are defined externally, stop may test for a sentinel
    value at the end of the iterator. Modifies deq and iterator
    *IN PLACE*. HISTORY 2018-01-17: modifed to return deq, stop
    when iterator is exhausted. Example:
    >>> d=deque([None]*3); it=iter(range(9))
    >>> throughto(d, it, lambda dd: dd[-1] == 7)
    deque([5, 6, 7])
    >>> throughto(d, it, lambda dd: dd[-1] == 42)
    deque([6, 7, 8])
    '''
    while not stop(deq):
        item = next(iterator, NoMore)
        if item is NoMore:
            break
        shiftin(deq, (item,))
    return deq

def throughtovalue(deq, iterator, key):
    '''Advances iterator and updates deque deq with values while
    the iterator is not exhausted and while a value greater than
    or equal to the key value has not been found. Modifies deq
    and iterator *IN PLACE*. If len(deq) > 1, iterator contains
    sorted (ascending) items, is increasing, and has sufficient
    items, the key value will be between the values of the last
    two items in the returned deq. Example:
    >>> d=deque([float('-inf')]*2); it=iter(range(9))
    >>> throughtovalue(d, it, 0)
    deque([-inf, 0])
    >>> throughtovalue(d, it, .2)
    deque([0, 1])
    >>> throughtovalue(d, it, 1)
    deque([0, 1])
    >>> throughtovalue(d, it, 1.2)
    deque([1, 2])
    '''
    return throughto(deq, iterator, lambda d: key <= d[-1])

def throughtoitem(deq, iterator, key):
    '''Advances iterator and updates deque deq *IN PLACE* with
    values while the iterator is not exhausted and while a value
    equal to the key value has not been found.
    '''
    return throughto(deq, iterator, lambda d: key == d[-1])

def lpopn(deq, n=1): ###
    '''Removes the left n items from deque deq and returns them as a list. We
    purposefully don't import deque; that should already have been done by the
    caller; if not, we want to produce the corresponding error.'''
    if n < 1:
        return []
    i, lst = n, []
    while i:
        lst.append(deq.popleft())
        i = i - 1
    return lst

def lpopuntil(lpoppable, test):
    while test(lpoppable):
        lpoppable.popleft()

def swab(deq, n=1):
    '''"Swab the deck!" Returns the deque deq after resizing *IN
    PLACE*. Resizing is accomplised as if items were
    removed from the left. Has no effect if n <= 0.'''
    assert isinstance(deq, deque)
    assert isinstance(n, int)
    while (n > 0) and (len(deq) > n):
        deq.popleft()
    return deq

def lcrop(deq, n=1):
    '''Deprecated. use swab'''
    swab(deq, n)

def lpop(deq, test=alwaysFalse):
    '''Repeatedly popleft-s the deque deq, as long as there are items remaining
    and the function test returns true.'''
    while len(deq) and test(deq):
        deq.popleft()

def _deal(deques):
    '''popleft-s the second item of the pair of deques (arg 0;
    could be a duple of deques or list of two deques) and
    appends it to the first item of the pair of deques.
        With analogy to turning the pages of a book, pages
    (items) are turned (popleft-ed) from the left side of
    the stack of pages to the right to the right side of
    the stack of pages to the left. Example:
            >>> deal((deque((0, 1)), deque((2, 3, 0, 1))))
            (deque([0, 1, 2]), deque([3, 0, 1]))
        See also: rotateleft
    '''
    if len(second(deques)):
        first(deques).append(second(deques).popleft())
    return deques

def rotateleft(deq):
    '''Rotates the items in the deque argument "left", by
    popleft-ing an item from the deque and appending it to the
    same deque. Returns the modified *IN PLACE* deque. c.f.
    primitive operations of many microcontrollers and
    microprocessors.'''
    return first(_deal((deq, deq)))

def rotateright(deq):
    '''Similar to rotateleft, but rotates the other direciton.'''
    if 2 < len(deq):
        deq.appendleft(deq.pop())
    return deq

def deal(deque_pair, test=lambda p: p[1] and p[1][0]): #TAGS pop append shift
    '''_deal-s while test (a function of deque_pair).
        With analogy to turning the pages of a book, pages
    (items) are turned (popleft-ed) from the left side of
    the stack of pages to the right to the right side of
    the stack of pages to the left. With analogy to an abacus,
    beads (items) are "slid" from right to left. Example:
        >>> deal((deque((0, 1)), deque((2, 3, 0, 5))))
        (deque([0, 1, 2, 3]), deque([0, 5]))
        If both items of deque_pair are the same deque, the net
    effect is rotation. 
    '''
    while test(deque_pair):
        _deal(deque_pair)
    return deque_pair

