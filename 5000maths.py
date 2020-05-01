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

def triangularsymmetricindex(ij):
    '''Returns the primary indices of a set of 2D cells where
    cells at indices (+/-i, +-/j) and (+/-j, +/-i) have the same
    value.  Originally intended for the case where only about
    1/8 of the values are actually stored in a lower triangular
    matrix-like sructure, as may be the case when storing
    distances from the centroid of a central cell.'''
    ija = tuplemap(abs, ij)
    return max(ija), min(ija)

