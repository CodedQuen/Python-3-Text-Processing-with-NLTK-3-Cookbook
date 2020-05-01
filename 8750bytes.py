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



def enumerate_non_ascii_bytes(byte_iterator):
    '''returns a filter that returns duples containing the
    relative position (beginning from zero) of the non-ASCII
    bytes found in the byte_iterator argument.
    '''
    return filterbytag(
        compose(
            partial(less, bytes((0x7f,))),
            second),
        enumerate(byte_iterator))

def next_non_ascii_byte(byte_iterator): #TAGS search
    '''If there are no more non-ascii bytes in the byte_iterator
    argument, returns (). Otherwise, returns a duple containing
    the relative position of the non-ascci byte, and (a copy of)
    the non-ascii byte itself.
    '''
    return next(enumerate_non_ascii_bytes(byte_iterator), ())

