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
################################### 'Stack' ###################################

####    'Nucleus' (Python)

S, R = [], []

#####   'Info' (Nucleus)

def empty():
    return not bool(len(S))

def tos():
    return S[-1]

def rtop():
    return R[-1]

def view():
    print('S: ', end='')
    for item in S:
        print(',',sep='',end=' ')
        print(item, end=' ')
    print()

####   'Manipulations-Basic' (Nucleus)

def pop():
    return S.pop()

def popR():
    return R.pop()


def push(x):
    S.append(x)

def pushR(x):
    R.append(x)

def lpush(lst):
    '''Don't abuse it.'''
    for item in lst:
        push(item)

def lpushR(lst):
    '''Don't abuse it.'''
    for item in lst:
        pushR(item)


def fromR():
    push(popR())

def toR():
    pushR(pop())


def swap():
    toR()
    dup()
    S[-2] = R[-1]

def dup():
    push(tos())

def drop():
    pop()

def ddrop():
    pop()
    pop()

def punch():
    swap()
    drop()

def over():
    toR()
    dup()
    fromR()
    swap()

def ddup():
    '2DUP'
    over(); over()

def popn():
    dup()
    if pop():
        dec()
        punch()
        popn()
    drop()
