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
from functools import partial

def genapply(iterable, function=ident): #DEPRECATED USE map
    '''returns a generator that yield-s the results of applying
    function to items of iterator.
    '''
    for item in iterable:
        yield function(item)

def do(function, *args, functions={}, **kwargs): ###
    try:
        function()
    except:
        return functions[function](args, kwargs)

def fofnonetofofany(function): ###
    '''Given a function of no arguments, returns another version
    of the function, which takes any number of arguments.'''
    def inner(*args, **kwargs):
        return function()
    return inner

def _compose(function, *functions): ###
    '''Returns a function that is the composition of the
    function arguments. The return performs the constituent
    function from right to left. Example: compose(hex, int)('3')
    returns '0x3'
    '''
    if functions:
        return lambda *args, **kwargs: function(_compose(*functions)(*args, **kwargs))
    else:
        return lambda *args, **kwargs: function(*args, **kwargs)

def affix(*strings): ###
    '''Returns the concatenation of the string arguments.
            >>> print(affix('left', '-', 'center', '-', 'right'))
            left-center-right
    '''
    return ''.join(strings)

def enclose(inner_string, left='', right=''): #.#
    '''Returns a string that is the concatenation of the left,
    inner_string, and right strings.
            >>> print(enclose('As you wish.', '``', "''"))
           ``As you wish.'' 
    '''
    return affix(left, inner_string, right)

def enclose_symmetric(inner_string, outer=''): #.#
    '''Returns a string that is the concatenation of outer,
    inner_string, and outer again.
            >>> print(enclose_symmetric('As you wish.', '"'))
            "As you wish."
    '''
    return enclose(inner_string, outer, outer)

def dunderfy(string): #.#
    '''Returns a string that is the concatention of '__',
    string, and '__' again.  Reference: https://wiki.python.org/
    moin/DunderAlias
            >>> print(dunderfy('name'))
            __name__
    '''
    return enclose_symmetric(string, '__')

#TODO setattrs SEEMS NOT TO WORK IN CONJUNCTION WITH compose WHEN doc IS SPECIFIED.
def setattrs(obj, **attributes): #.#
    for attribute in filter(lambda a: hasattr(obj, a), attributes):
        setattr(obj, dunderfy(attribute), attributes[attribute])
    return obj

def compose(function, *functions, **attributes): #.#
    '''Same as _compose, except, in addition, one may optionally
    set the attributes. Double underscores (dunders) are attached to the
    names of the attributes listed. References: setattr https://
    docs.python.org/3/library/functions.html#setattr , dir
    https://docs.python.org/3/library/functions.html#dir ,
    attributes https://stackoverflow.com/questions/50370917/
    what-is-the-best-way-in-python-to-write-docstrings-for-
    lambda-functions#50371184
            >>> decimal_len = compose(len, str,
            ... name='decimal_len', doc=condense("""Returns the
            ... length of the decimal representation of the int
            ... argument."""))
            >>> help(decimal_len)
            Help on function decimal_len in module __main__:

            decimal_len(*args, **kwargs)
            Returns the length of the decimal representation of the int argument.
    '''
    lam = _compose(function, *functions)
    keys = tuple(attributes.keys())
    print(*map(dunderfy, keys))
    setattrs(lam, **attributes)
    return lam

def rcompose(function, *functions, **attributes): #.#
    '''Same as compose, but the functions are applied left to
    right.
            >>> rcompose(len, str)('42')
            '2'
            >>> # NOTE THE QUOTES: THE str OF THE len, NOT THE
            >>> # len OF THE str.
            '''
    return compose(
        *reversed(tuple(
                chain( (function,), functions )   )),
        **attributes)

def setargdatum(function, datum): ###
    '''Given a function and a datum, returns a modified version
    of the function, where the datum of the first argument is
    adjusted.'''
    def inner(n, *args, **kwargs):
        return function(n - datum, *args, **kwargs)
    return inner

def argswap(function): ###
    return lambda arg0, arg1, *args, **kwargs: function(arg1, arg0, *args, **kwargs)

def postfix(arg, *functions): #.#
    '''postfix(value, f, g, h) returns the same result as h(g(f(value)))'''
    return rcompose(*functions)(arg)

def postfix(arg, *functions): #.#
 assert isinstance(arg, tuple), 'First argument must be tuple.'
 assert len(arg) < 3, 'Argument must contain two or fewer items.'
 fn = rcompose(*functions)
 if len(arg) == 2:
  assert isinstance(arg[0], tuple), 'First item in argument must be tuple.'
  assert isinstance(arg[1], dict), 'Second item in argument myst be dict.'
  return fn(*arg[0], **arg[1])
 if len(arg) == 1:
  assert isinstance(arg[0], tuple) or isinstance(arg[0], dict), 'Argument of length 1 must contain tuple or dict.'
  if isinstance(arg[0], tuple):
   return fn(*arg[0])
  if isinstance(arg[0], dict):
   return fn(**arg[0])
 return fn()

def group(*items): ###
    '''Example: group(1, 2) returns (1, 2). HISTORY 2018-09-17: formerly retured a list.'''
    return tuple(items)

def applyfx(fx): ###
    f, x = fx; return f(x)

def zipapply(functions, args): #.#
    '''Evaluate each function in functions for each argument in
    args (one-to-one). Return the results as a tuple. Example:
    zipapply((str, hex, bin), (1,1,1)) returns ('1', '0x1',
    '0b1'). HISTORY 2018-01-05: changed the return from list to
    tuple.'''
    return tuple(map(applyfx, zip(functions, args)))

def star(function): ###
    '''Given a function of one argument and optional arguments,
    returns a function of many positional arguments and the
    optional arguments. Example: star(list)(1, 2, 3) returns
    [1, 2, 3]'''
    def starred(*args, **kwargs):
        return function(args, **kwargs)
    return starred

def unstar(fn): ###
    '''Creates a single-argument funtion from a multi-argument
    function. The single argument is a compound argument whose
    content is equivalent to multiple arguments. Example:
    >>> unstarredzip = unstar(zip)
    >>> tpl = range(3), range(3)
    >>> list(unstarredzip(tpl))
    [(0, 0), (1, 1), (2, 2)]
    >>> # compare:
    >>> list(zip(tpl))
    [(range(0, 3),), (range(0, 3),)]
    '''
    def unstarred(args, **kwargs):
        return fn(*args, **kwargs)
    return unstarred

