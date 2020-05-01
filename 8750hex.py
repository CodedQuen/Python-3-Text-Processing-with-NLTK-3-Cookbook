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

def loadhex(filename, wordsize=1):
    '''Loads the entire file specified by filename. Only
    characters in the ASCII range are anticipated. Nongraphic
    characters (e.g., space, end-of-line) are ignored. Values
    are converted to unsigned integers, assuming they are
    represented in the file as sequences of hexadecimal digits
    [0-9A-Fa-f]; all values must be represented with the same
    number of bytes, according to wordsize. A partial values at
    the end of the file are ignored (e.g., as in the case where
    wordsize=2 and there are an odd number of hexadecimal digits
    in the file.). If any graphic character is not a hexadecimal
    digit, error occurs.'''
    return mapchain(
        filter(
            lambda s: len(s) == wordsize,
            groups(
                filter(
                    isgraph,
                    iter(freadentire(filename))),
                wordsize)),
        unstar(join),
        partial(int, base=16))

