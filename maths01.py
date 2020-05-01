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
# math PACKAGE "EXTENSIONS"
from math import isinf, isnan

def precise_sum(iterable):
    '''Future: cancel equal-magnitude, opposite sign values;
    cancel partial sums.'''
    values = tuple(iterable)
    nsum = sum(sorted(list(filter(less,     values              )), reverse=True))
    psum = sum(sorted(list(filter(un(less), filter(None, values)))              ))
    return nsum + psum

def pulse(period, function=partial(tuple.__getitem__, (0, 1))):
    '''Binary Pulse. Returns a map that produces a periodic
    signal using the values function(False) and function(True).
    The 'True' value will be produced every period-th time: the
    'False' value is produced otherwise. Example:
    ''.join(map(str, quota(pulse(3), 9))) == '001001001'
    '''
    return map(function, map(un(bool), skip(cycle(period))))

def cap(upperbound, x):
    return x if (x <= upperbound) else upperbound

def prop(lowerbound, x):
    return x if (lowerbound <= x) else lowerbound

def clamp(lowerbound, upperbound, x):
    return cap(prop(x, lowerbound), upperbound)

def clip(x, lo=-Inf(), hi=Inf()):
    '''Returns the primary argument if it is between the hi and
    lo values. Returns the lo value if x is lower. Returns the
    hi value if x is higher.'''
    return lo if x < lo else x if x <= hi else hi

def strformatfloat(fmt, f, specialwidth=5): ### tags: str format float nan inf
    '''Returns a string representation of a float using the format fmt
    (arg 0) for numeric values, "nan" for nan-s, repr(f) for
    +/-inf. HISTORY: 2018-07-23: added optional argument width.'''
    from math import isinf, isnan
    sfmt = '{0:>' + str(specialwidth) + '}'
    return sfmt.format('nan') if isnan(f) else \
            sfmt.format(repr(f)) if isinf(f) else \
                    fmt.format(f)

def isscalar(x):
    '''Returns a bool indicating whether the argument is a
    scalar quantity, where infinites and NaN-s are not
    considered scalars.'''
    if isint(x):
        return True
    return isfloat(x) and not isinf(x) and not isnan(x)

def iscomplex(x): ###
    return isinstance(x, complex)

def isnegativeint(i):
    if not isint(i):
        return False
    return i < 0

def isnegativefloat(x):
    if not isfloat(x):
        return False
    if x == -0.:
        return True
    return x < 0.

def isnegativecomplex(z):
    if not iscomplex(z):
        return False
    if not (z.imag == 0.):
        return False
    return z.real < 0.

def isnegative(x):
    return isnegativeint(x) or isnegativefloat(x) or isnegativecomplex(x)

def signint(n):
    nn = int(n)
    if not nn:
        return 0
    return (-1, 1)[0 < nn]

def istuple(x):
    return isinstance(x, tuple)

def istupleofpositiveints(x):
    if not istuple(x) or not all(map(isint, x)) or any(map(partial(int.__ge__, 0), x)):
        return False
    return True

def istuplesmaller(x, n):
    return istuple(x) and len(x) < n

def istupleoflen(x, n):
    return istuple(x) and len(x) == n

def istuplelarger(x, n):
    return istuple(x) and len(x) > n

def istuplesized(x, n, restraint):
    '''Returns a bool indicating whether x is a tuple of the
    size specified. The restraing argument is an int; only the
    sign is significant: if negative: tuple is tested for having
    a len less than n, if zero: tuple is tested for having a len
    equal to n, if positive: tuple is tested for having a len
    greater than n. "---What about the [TOUS]es? ---[Tuples] of
    unusual size? I don't think they exist."'''
    assert isint(n)
    assert isint(restraint)
    return (istuplesmaller, istupleoflen,
            istuplelarger)[1+signint(restraint)](x, n)

def isfloatnumber(x): #.# tags: isfloatnumber
    '''History: 2018-01-12: changed name from isfloatnumber.'''
    if not isfloat(x):
        return False
    from math import isinf, isnan
    return not (isinf(x) or isnan(x))

def iscomplex(x): ### tags: iscomplexnumber
    '''History: 2018-01-12: changed name from iscomplexnumber.'''
    if not iscomplex(x):
        return False
    from cmath import isinf, isnan
    return not (isinf(x) or isnan(x))

def isnumber(x):
    return any(multifunction(isint, isfloat, iscomplex)(x))

def roundfloor(x):
    '''Returns a float equal to x rounded to the nearest
    integer, consistent with the floor function (i.e. "0.5
    rounds up.")'''
    assert isfloat(x)
    from math import floor
    return floor(x + 0.5)

'''
def product(a, b): #REMOVED
    assert False, 'product(a, b) removed. use product(iterable).'
'''

def sums(iterables): ###
    return map(sum, iterables)

def diff(seq): ###
    return seq[1] - seq[0]

def difference(a, b): ###
    return a - b

def vectordifference(iterable0, iterable1):
    '''Returns a map of the differences between corresponding
    elements of the two iterable arguments. Example:
    tuple(vectordifference((3,5), (1,2))) == (2, 3)'''
    return map(unstar(difference), zip(iterable0, iterable1))

def relativevectors(vector, vectors):
    '''Returns a map of maps. Each outer map is a vector
    difference between vector and one of the vectors produced by
    the vectors argument. Each inner map is a vector. Expect
    strange results if vector is not persistent. Example:
            >>> tuplemap(tuple, relativevectors((3,4), ((0,0), (9,0), (0,9))))
            ((3, 4), (-6, 4), (3, -5))
    '''
    return map(vectordifference, steady(vector), vectors)

def deltas(vector, vectors): #TAG difference
    '''Similar to relativevectors, except that each item
    produced by vectors must be finite. Example:
            >> tuple(deltas((3,4), ((0,0), (9,0), (0,9))))
            ((3, 4), (-6, 4), (3, -5))
    '''
    return map(tuple, relativevectors(vector, vectors))

def quadrance(vector):
    '''Returns the quadrance between the point represented by
    the vector argument and the origin.'''
    return sum(map(square, vector))


def diffs(iterable):
    'Returns an iterator over the differences between the first item and any remaining items.'
    assert False, 'maths.py: diffs: Needs to be rewritten.'
    it = iter(iterable)
    for item in it:
        first = item

def divideby(divis, divid): ###
    '''Note the order of the arguments! Returns divid / divis.
    Designed for implementation using partial.'''
    return divid/divis

#def div

def vectorsum(*iterables):
    '''Returns a map of sum-s of corresponding elements of
    iterables. Example:
    >>> tuple(sumvector(range(9), range(9)))
    (0, 2, 4, 6, 8, 10, 12, 14, 16)
    '''
    return map(sum, zip(*iterables))

'''
def sumvector(*iterables): #DELETED use vectorsum
'''

def multscalar(scalar, iterable): # tags: scalar product
    '''Returns a map of values that together form the result of
    scalar multiplication of the vector represented by the
    iterable of scalars. Example:
    >>> tuple(multscalar(3, range(9)))
    (0, 3, 6, 9, 12, 15, 18, 21, 24)
    '''
    def prod(x):
        return scalar * x
    return map(prod, iterable)

def intervalfwd(start, width=1): ###
    '''Given a scalar value representing the beginning of an
    interval, returns a duple representing the same interval.'''
    return start, start + width

def intervalsfwd(iterable, width=1): #.#
    '''The iterable argument produces scalars. Returns an
    iterable of the corresponding forward intervals.'''
    return map(partial(intervalfwd, width=width), iterable)

def interp_const(knowns, x):
    '''Returns the weights to use for linear interpolation at
    sclar numeric value x, given the x-coords of two known
    points, stored as the duple of scalars, knowns.
    >>> interp_const((0, 1), 0.5)
    (0.5, 0.5)
    >>> interp_const((85, 255), 192)
    (0.37058823529411766, 0.62941176470588234)
    >>> interp_const((85, 255), 34)
    (1.3, -0.29999999999999999)
    '''
    return (NaN(), NaN()) if equal(*knowns) else \
            tuple(map(
                    partial(divideby, diff(knowns)),
                    (knowns[1] - x, x - knowns[0])))

def interp_lin(knowns, find, index=0):
    '''The duple knowns contains two aligned objects, each of
    which may be converted tuples of scalar, numeric
    values. The unknown argument is a scalar value correpsonding
    to one of the indices of known. Returns the interpolated
    value. Conceptually, each element of knowns is a vector. Example:
    >>> tuple(interp_lin(((0, 0, 6), (1, 45, 12)), .5))
    (0.5, 22.5, 9.0)
    >>> # index defaults to int(0), .5 is halfway between the
    >>> # values indexed at 0 (which are 0 and 1). The resultant
    >>> # tuple has values halfway between the given values.
    >>> #
    >>> tuple(interp_lin(((0, 0, 6), (1, 45, 12)), 15, 1))
    (0.33333333333333331, 15.0, 8.0)
    >>> # index is specified as int(1). 15 is one-third of the
    >>> # way between the values indexed at 1 (which are 0 and
    >>> # 45). The resultant tuple has values one third of the
    >>> # way from the first to the second set of values.
    >>> #
    >>> tuple(interp_lin(((0, 0, 6), (1, 45, 12)), 1/3))
    (0.33333333333333331, 15.0, 8.0)
    >>> # index defaults to int(0). 1/3 is one-third of the way
    >>> # between the values indexed at 0 (which are 0 and 1).
    >>> # The resultant tuple has values one-third f the way
    >>> # from the first to the second argument.
    '''
    k0, k1 = map(tuple, knowns) # tuple(knowns[0]), tuple(knowns[1])
    w = interp_const((k0[index], k1[index]), find) # weights
    return tuple(sumvector(multscalar(w[0], k0), multscalar(w[1], k1)))

def interp_consts(knowns, exes, srch=bsearch_lt):
    '''Similar to interp_const, but finds interpolation constants for all the exes.'''
    printerr('(STATUS)', 'interp_consts:')
    xx = tuple(exes)
    knowns = tuple(knowns)
    #printerr('(STATUS)', 'interp_consts: xx:', xx)
    #printerr('(STATUS)', 'interp_consts: knowns:', knowns)
    #betweens = tuple(map(lambda x: (knowns[x[0]], knowns[x[1]]), search_each(knowns, xx)))
    #printerr('ic: bt:', betweens)
    printerr('ic: xx:', xx)
    printerr('ic: knowns:', knowns)
    #l=list(map(lambda z: interp_const(*z), zip(betweens, xx)))
    #print('ic: ics:', l)
    return map(unstar(interp_const), zip(knowns, xx))

def interpolated_values(xy, x):
    '''Given xy, an iterable of ordered pairs (x, y), and x, an
    iterable of scalar values for which to determine the
    corresponding y-values, returns an iterator of the ordered
    pairs of interpolated values.'''
    def exes(segment):
        return first(first(segment)), first(second(segment))
    def wyes(segment):
        return second(first(segment)), second(second(segment))
    x = iter(x)
    segments = zipself(xy)
    currentsegment = more(segments)
    currentx = more(x)
    while   (currentx       is not NoMore) and \
            (currentsegment is not NoMore):
        ic = interp_const(exes(currentsegment), currentx)
        if second(ic) < 0: # x is to the left of the current segment
            yield currentx, NaN()
        elif 0 <= min(ic): # x is in the current segment
            yield currentx, dot((ic, wyes(currentsegment)))
        else: # x is to the right of the current segment and might be found later
            pass
        if first(ic) < 0: # x is to the right
            currentsegment = more(segments)
        else: # x is to the left of or in this segment
            currentx = more(x)
    for ex in x:
        # we have gone through all of the segments and still
        # have exes.
        yield ex, NaN()

def betweenx(x, y, z):
    'exclusive between'
    return (x < y) and (y < z)

def betweenl(x, y, z):
    'left-inclusive, right-exclusive between'
    return (x <= y) and (y < z)

def betweenr(x, y, z):
    'left-exclusive, right-inclusive between'
    return (x < y) and (y <= z)

def between(x, y, z):
    '''Returns a bool telling whether y is between x and z. See
    also betweeni, betweenl, betweenr, and betweenx. Reference:
    Insall, Matt. "Strictly Between." From MathWorld--A Wolfram
    Web Resource, created by Eric W.  Weisstein.
    http://mathworld.wolfram.com/StrictlyBetween.html'''
    return (x <= y) and (y <= z)

'''
def betweeni... # inclusive between
'''
betweeni = between

def allequal(iterable):
    it = iter(iterable)
    item0 = next(it, NoMore)
    if item0 is NoMore:
        return True
    return all(map(partial(equal, item0), it))

def series(function, iterable): ### tags: infinite series
    '''Internally, iterable is enumerate-d. The function
    argument should be a function of two arguments. If iterable
    is finite or cut off at some point, could be used to compute
    a partial sum. Example:
    >>> print(*series(unstar(argswap(pow)), (2,)*5))
    1.0 2.0 4.0 8.0 16.0
    '''
    return map(function, enumerate(iterable))

def partialsum(function, iterable): #.# tags: infinite series
    '''Example:
    >>> print(partialsum(unstar(argswap(pow)), (2,)*5))
    31.0
    '''
    return sum(series(function, iterable))

def squares(iterable):
    '''Returns a map of the squares of the iterable argument.'''
    return map(square, iterable)

def quadrance(vector):
    '''Returns the sum of the squares of the values produced by the
    iterable argument, equal to the quadrance between the origin
    and the point represented by the argument.  Example:
    sumofsquares1(range1(4)) == 30'''
    return compose(sum, squares)(vector)

def vectornorm(vector, power=2): #TAGS distance length
    '''Returns the vector norm of the vector argument.  sum of
    the squares of the values produced by the iterable argument,
    equal to the quadrance between the origin and the point
    represented by the argument.  Example:
    sumofsquares1(range1(4)) == 30'''
    assert power == 2, 'vectornorm not yet defined for power != 2.'
    from math import sqrt
    return compose(sqrt, quadrance)(vector)

def distance(vector):
    return vectornorm(vector)

def vectornorms(vectors, power=2):
    return map(partial(vectornorm, power=power), vectors)

def inversedistancesquared(vector):
    return compose(reciprocal, quadrance)(vector)

def inversedistancesquared(vector):
    assert False, ''

def sumofsquares(compounditerable):
    ''''''
    #printerr('sumofsquares:')
    return mapchain(compounditerable, squares, sum)


def vectorwrite(text_file, string_iterable, columns=1):
    '''write-s the strings in string_iterable to text_file.
    Newline characters are inserted so that no more than columns
    values appear on the last line, and columns values appear on
    any preceeding lines.'''
    fwriteall(text_file, fmtw(string_iterable, n=columns))

def pseudocos2(x):
    '''Reurns an approximate value of cos-2 (x * pi/2), from a
    polynomial approximation valid in [-1, 1]. see also:
    Docs/maths-pseudocos2.pdf'''
    return (x - 1) ** 2 * (x + 1) ** 2

def windowed(function, lo=-Inf(), hi=Inf()):
    '''Return a windowed version of a numeric function. The
    returned function behaves as the primary argument when its
    argument is in [lo, hi). However, when the returned
    function-s argument is less than lo, or greater than hi, its
    return is 0 cf.  https://en.wikipedia.org/wiki/Window_function
    HISTORY: 2019-02-28 changed to be exclusive of "hi."'''
    def inner(x):
        return 0 if x < lo else function(x) if x < hi else 0
    return inner

def normalize(iterable, shift=0, factor=1, divisor=1):
    '''Returns a map of normalized numeric values. For each item
    x produced by iterable, the return produces
    (x - shift) * factor / divisor. Reminder: for generic
    normalization, use map.'''
    return mapchain(iter(iterable),
        partial(argswap(difference), shift),
        partial(product, factor),
        partial(argswap(quotient), divisor))

sumproduct = compose(sum, arrayproduct)

def weightedaverage(values, weights):
    return sumproduct(values, weights) / sum(weights)
