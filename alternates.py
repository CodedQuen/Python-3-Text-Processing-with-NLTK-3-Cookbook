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
def sdmi(arg, functions):
    '''Single Data, Multiple Instructions. Evaluates functions
    for arg. Returns a corresponding tuple.'''
    return zipapply(functions, (arg,) * len(functions))

def alternate(functions, function, arg):
    '''Form a tuple of values by applying the functions in the
    functions argument (a tuple of functions) to arg.
    Use this tuple as an argument for function. Return the
    result of function. Originally intended to develop a
    function to return an int if the corresponding floating
    point value has no fractional part.'''
    return function(sdmi(arg, functions))

def preferint(functions):
    '''The functions argument is a tuple of functions, which, at
    least conceptually, have the possibility of returning the
    same value for the same input, but may represent that value
    in different ways, for example floating-point division and
    integer division. Returns a function that, in turn, returns
    the int value if all values are equal, otherwise returns the
    first value that is not an int. Example:
    >>> foo = preferint((lambda x: x/60, lambda x: x//60))
    >>> print(foo(59), foo(60))
    0.983333333333 1
    >>> # Of course, it it possible to create something non-
    ... # sensical:
    >>> bar = preferint((lambda x: False, lambda x: x//60))
    >>> print(bar(1))
    False
    '''
    def evaluate(tpl):
        if allequal(tpl):
            return tpl[next(which(map(isint, tpl)))]
        return tpl[next(which(mapchain(tpl, isint, fnnot)))]
    def inner(x):
        return partial(alternate, functions, evaluate)(x)
    return inner
