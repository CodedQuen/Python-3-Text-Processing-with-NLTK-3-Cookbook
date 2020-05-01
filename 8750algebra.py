# Text Processor
# Copyright (C) 2019 D. Michael Parrish
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

def functionproduct(*functions):
    '''Returns a function whose return is the product of the
    returns of the functions:
            (f * g * h * ...)(x) =
            f(x) * g(x) * h(x) * ....
    '''
    return lambda *args, **kwargs: unstar(product)(
        multifunction(*functions)(*args, **kwargs))

def functionproducts(iterable, *functions):
    '''Forms a function product from functions and returns a map
    of the resultant function values by applying the function
    values.
    '''
    return map(functionproduct(*functions), iterable)

