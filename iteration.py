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
'''Iteration
Dependencies: triv.py
'''
def iterate(function, test, iterations=-1): ###
    while iterations:
        iterations -= 1
        y = function()
        if test(y):
            break
    return y

def dequpdate(deq, function):
    assert 1 < 0, 'placeholder only'

def fixedpoint(f, x, n=-1, comp=equal):
    '''fixed point iteration with funciton f, initial value x,
    max number of iterations n, and comparison function comp.
    Examples:
    fixedpoint(lambda s: s.replace(' '*2, ' '), 'this   is   a   test.')[0]
    form math import cos
    fixedpoint(cos, 1.) # dangerous, because testing floating points for equality.
    fixedpoint(cos, 1., comp=lambda x, y: abs(x-y) < 2**-10) # 
    Note: SICP presents more efficent methods for numerical
    functions (see "Finding fixed points of functions,"
    therein).  '''
    while True:
        y = f(x)
        if not n or comp(x, y):
            break
        n -= 1;   x = y
    return x, y, n
