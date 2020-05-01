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



def tail_is_non_ascii(file):
    '''returns a bool indicating whether any of the remaining
    bytes (i.e., the "tail") in the file (open for binary
    reading) are non-ASCII bytes.
    '''
    print(phrase(words('''
        **** WARNING **** tail_is_non_ascii: During tests, not
        all files containing non-ASCII bytes were identified as
        such.''')))
    return bool(next_non_ascii_byte(fbytes(file)))
