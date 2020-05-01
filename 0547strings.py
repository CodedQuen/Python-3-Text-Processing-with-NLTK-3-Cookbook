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



def strsplit_ranges(string, sep, maxsplit=-1):
    '''yield-s ranges of indices of substrings of string that
    1) are separated by sep, AND INCLUDE sep as the final
    character and 2) itentify any trailng characters (i.e., when
    the last element of string is not equal to sep)

    The maxsplit argument is not used.

    FUTURE
    
        -   maxsplit will be used in a manner analogous to
            str.split.

        -   handle whitespace in a manner similar to str.split.

    SEE ALSO strsplit_
    '''
    for rng in ranges_contiguous(chain(
            map(add1, strfindall(string, sep)),
            entuple(len(string)) )):
        if not len(rng):
            return
        yield rng

def strsplit_(string, sep='\n', maxsplit=-1):
    '''yield-s substrings of string separated by the sep. The
    **** sep string is INCLUDED **** as the tail of each
    yield-ed substring (which is the main design feature of this
    def)., except in the case where the string does not end in
    sep.
    
    similar to str.split, except that the sep character is
    preserved and maxsplit is not used.

    **** THE CORRESPONDING SUBSTRINGS **** are yield-ed, not
    returned all together in one list, as with str.split.

    FUTURE
    
        -   maxsplit will be used in a manner analogous to
            str.split.

        -   handle whitespace in a manner similar to str.split.
    '''
    for rng in strsplit_ranges(string, sep, maxsplit):
        yield string[min(rng):1 + max(rng)]

