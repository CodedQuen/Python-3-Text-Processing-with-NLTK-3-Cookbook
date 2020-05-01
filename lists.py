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

def cardinalindex(sequence, index, default=None):
    if not rangecheck(sequence, index):
        return default
    elif index < 0:
        return len(sequence) + index
    return index

def poplist(List, index): #TAGS extend unextend
    '''Somewhat the opposite of extend. Modifies *IN PLACE* the
    List argument. For a valid index, removes and returns the
    end of the list beginning at index. For an invalid index,
    returns a new empty list, leaving the List unmodified.'''
    icard = cardinalindex(List, index, -1)
    if icard < 0:
        return []
    return list(reversed(tuple(map0(List.pop, range(len(List) - icard)))))

def uninsert(List, index):
    '''Similar to remove, but removes by index rather than
    value. Returns the modified *IN PLACE* List. Has no effect
    if the index is invalid. Example:
            >>> uninsert(list(range(9)), 1) # NOTICE NO 1
            [0, 2, 3, 4, 5, 6, 7, 8]
    '''
    icard = cardinalindex(List, index, -1)
    if icard < 0:
        return List
    tail = poplist(List, index)
    return List + tail[1:]

def thread(extensible, iterator, n=1):
    '''*IN PLACE* The iterator is "thread-ed" through
    extensible.  If possible, advances iterator, appending the
    corresponding n item(s). Returns extensible.
        It is possible to determine whether another item was
    extracted from iterator by comparing the length of
    extensible before and after the call, provided no other
    process has modified extensible in the meantime.
        Before (the pipe indicates the "boundary" between the
        next item of the iterator and the last element of
        appendable):
            rest of extensible ... [A] [B] [C] | [D] [E] [F] ... rest of iterator
        After:
        rest of extensible ... [A] [B] [C] [D] | [E] [F] ... rest of iterator
    '''
    return extend(extensible, quota(iterator, n))

def sorted(lst, key=None, reverse=False):
    '''Returns a sorted copy of the list argument.'''
    l = deepcopy(lst)
    l.sort(key=key, reverse=reverse)
    return l

def lreversed(lst): #OLDNAME reversed
    '''Reverses the list *IN PLACE*. Returns the list.'''
    lst.reverse();   return lst

def build(item):
    '''Example:
    >>> lst = []
    >>> mor = build(lst)
    >>> mor(1)
    [1]
    >>> mor(42)
    [1, 42]
    '''
    return partial(append, item)

def listclear(lst):
    '''Substitute for list.clear, added in Version 3.3'''
    while lst:
        lst.pop()

def popuntil(poppable, test):
    while not test(poppable):
        poppable.pop()
        
def swap(lst, i=0, j=1):
    '''Swap the first two elments of a list or other list-like mutable
    structure *IN PLACE*. Returns the modified list. Has no
    effect on lists containing fewer than two elements.'''
    if len(lst) < 2:
        return lst
    lst[i], lst[j] = lst[j], lst[i]
    return lst

def lstsplitn(lst, n=1):
    '''Returns the items of list lst reorganized into two parts. Originally
    intended for cases where 0 < n < len(lst) and n > 1'''
    return [lst[:n], lst[n:]]

def sublist(lst, ind):
    'Return a new list, which contians the elements of lst specified by ind.'
    nls = []
    for i in ind:
        nls.append(lst[i])
    return nls

def flattenlist(lstlst):
    '''lstlst is a list of lists. returns a new list contianing
    the contents of the interior lists of lstlst.  For example,
    [[1, 2], [3, 4]] becomes
    [1, 2, 3, 4].'''
    ret = []
    for lst in lstlst:
        for item in lst:
            ret.append(item)
    return ret

def listlist(n=1):
    'Returns a list of length n, where each element is an empty list.'
    return [ [] for i in range(n) ]

def appendall(appendables, toappend):
    #printerr('appendall: appendables:', appendables)
    #printerr('appendall: toappend:', toappend)
    for thing in zip(appendables, toappend):
        #printerr('appendall: thing:', thing)
        first(thing).append(second(thing))

def fill(obj, fillobj=None, n=0):
    '''Conditionally modifies obj (typically a list or deque)
    *IN PLACE* by appending fillobj values such that the modified
    obj has length of at least n. Only when the unmodified obj
    has length of at least n will the obj not be modified.
    Returns the modified obj. Examples:
            >>> fill([])
            []
            >>> l = [1];   fill(l, n=4)
            [1, None, None, None]
            >>> l
            [1, None, None, None]
            >>> fill(l, -5)
            [1, None, None, None]
    '''
    obj.extend((fillobj,) * (n - len(obj)))
    return obj
