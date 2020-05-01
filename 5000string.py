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

def words(string='', sep=None):
    '''Returns a tuple of words derived from the string
    argument. Cf. str.split. HISTORY: 2019-01-14: added optional
    sep argument. 2018-04-10: formerly returned a list.
    '''
    if sep is not None:
        return tuple(string.split(sep))
    return tuple(string.split())

towords = words #DEPRECATED use words

def phrase(string_iterable, sep=' '):
    '''Similar to str.join, but with the arguments reversed.
            >>> phrase(('As', 'you', 'wish.'))
            'As you wish.'
    '''
    return sep.join(string_iterable)

joinwords = phrase #DEPRECATED use phrase
