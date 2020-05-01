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
def carttoraster(gen, dims=(0,), nodata=0, eol=(True,)):
    '''Receives ordered tuples from gen. Each tuple has the Cartesian
    coordinates of a cell value followed by the cell value itsef. Cell values
    must be strings. produces a raster from tuples of locaitons and cell values.

    ijz: item yielded by gen, tuple containing Cartesian coords consistent with
    ???
    
    
    '''
    k=0
    dims1 = list(map(lambda x: x - 1, dims))
    crd = genlimit(counter(dims), items=product(dims)) 
    for ijz in gen:
        for c in crd: # yield all values preceeding ijz
            if c == first(ijz):
                break
            yield nodata # c, nodata
        yield second(ijz) # ijz
    for c in crd: # yield all values coming after last ijz
        yield nodata # c, nodata


#f=openw('t:/junk')
#from random import random
#for item in quota(map(lambda x: random(), indefinite()), 512*553):
    #nul = f.write(' '+fmtspecsimple('f4').format(item))

#f.close()
##
def vectorstream(f, function=float, parse=towords):
    return map(function, stream(iter(f), parse=parse))

vectorread = vectorstream #DEPRECATED use vectorstream

def arrayquotient(dividend, divisor):
    '''Returns a map containing the quotients of the
    corresponding items in the iterables divident (arg 0) and
    divisor (arg 1).'''
    return map(quotient, dividend, divisor)

def arrayweightedaverage(weights, *vectors):
    '''Typically, the number of items in the iterable weights is
    equal to the number of optional positional arguemtns, each
    of which should be iterable. Example:
    >>> tuple(arrayweightedaverage((.2, .8), (0, 0, 10), (10, 20, 30)))
    (8.0, 16.0, 26.0)'''
    return map(sum, zip(*tuple(map(multscalar, weights, vectors))))

# f=open('p:/exec-all.py');   exec(f.read());   f.close()

#
#f = open('t:/junk')
#r = vectorread(f)
#f.close()
