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

def lsb(integer): #TAGS byte bits least significant byte
    '''"least significant byte."
    
    For nonnegative int-s, returns an unsigned int that is
    consistent with the lower eight bits of its base-2 (binary)
    representation.
    
    FUTURE: returns values for negative int-s. **** DRAFT ****
    help follows...  For integers in [-127, 0), returns an
    unsigned int that is the two-s complement of the
    corresponding integer value.
    '''
    assert isinstance(integer, int)
    assert -1 < integer
    return integer % 256

