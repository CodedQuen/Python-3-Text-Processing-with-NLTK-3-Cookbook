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
def condense(string): #TAGS whitespace format
    '''Returns a string fomred from the characters of the string
    argument, except the excess whitespace characters. The final
    newline character of the argument will be preserved, if
    present.
            >>> condense("""
            ... As
            ...
            ... you
            ...
            ... wish.
            ... """)
            'As you wish.\n'
            >>> condense('As   you   wish')
            'As you wish'
    '''
    return string if not string else (
        phrase(words(string)) + (
            NEWLINE if last(string) == NEWLINE else NULL))

