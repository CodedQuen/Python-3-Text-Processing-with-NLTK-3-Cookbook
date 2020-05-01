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
def foo():
    def inner():
        class NoneYet:
            def __init__(self):
                return 
            def __repr__(self):
                return 'NoneYet'
        class NoMore:
            def __init__(self):
                return 
            def __repr__(self):
                return 'NoMore'
        yield NoneYet()
        yield NoMore()
    def get(which):
        singletons = tuple(inner())
        return sgl[which]
    while True:
        yield


    

        return\
def gen(switch):
        ny = NoneYet()
        nm = NoMore()
        while True
            yield NoMore if switch else NoneYet



def shiftin(deq, iterator): ### tag: ASL left shift <<
    '''Returns a modified *IN PLACE* version of deque deq, where
    items have been shifted to the left, the item origially at
    the initial position has been removed, and a new item (if
    available from iterable) has been appended. c.f.
    deque.extend. TO DO: when shiftout needed: refactor to
    shift, shiftin, shiftout.'''
    lgt = len(d)
    thread(deq, iterator)
    if lgt < len(d):
        deq.popleft()
    return deq

def recall(deq, iterator):
    if deq:
        return deq[-1]
