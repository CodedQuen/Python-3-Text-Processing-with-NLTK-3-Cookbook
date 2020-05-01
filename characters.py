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

CHARACTER_SET_ORDS_STDOUT = range(0xff) #110000)
CHARACTER_SET_ORDS_STDERR = range(0xff) #110000)

BINARY_DIGITS  = '01'
OCTAL_DIGITS = BINARY_DIGITS + '234567'
DECIMAL_DIGITS = OCTAL_DIGITS + '89'
HEX_DIGITS = DECIMAL_DIGITS + 'ABCDEF' + 'abcdef'

printerr('characters.py (A)')

def allcharacters(among=CHARACTER_SET_ORDS_STDOUT, file=stdout):
    '''Returns a dict of character vs. Unicode code point. All
    code points are considered. Side effect: valid characters
    are print-ed to standard error.'''
    def ch(u):
        try:
            c = chr(u)
            printerr(c if c else '', end='')
        except:
            c = ''
        return c
    return tuple(filter(lambda duple: duple[1], enumerate(map(ch, among))))

printerr('characters.py (B)')

printerr(condense('''
    Building character tables. This could take a little while.
    The allcharacters function is attempting to print each
    character to stdout and stderr. **** EXPECT **** to see
    "garbage" characters on stdout and stderr.'''))

TEMP_MSG = 'Building character table for', '(', 'candidate characters).'

printerr('characters.py (B)')

printerr(TEMP_MSG[0] + 'stdout', TEMP_MSG[1],
    str(count(CHARACTER_SET_ORDS_STDOUT)), TEMP_MSG[2])
CHARACTER_TABLE_STDOUT = allcharacters(among=CHARACTER_SET_ORDS_STDOUT)

printerr('characters.py (C)')

printerr(TEMP_MSG[0] + 'stderr', TEMP_MSG[1],
        str(count(CHARACTER_SET_ORDS_STDERR)), TEMP_MSG[2])
CHARACTER_TABLE_SDTERR = \
        allcharacters(among=CHARACTER_SET_ORDS_STDERR, file=stderr)

printerr('characters.py (D)')
 
del TEMP_MSG


def character_chart_character_ord(
        character_table=CHARACTER_TABLE_STDOUT,
        subrange_iterator=iter(range(128))):
    '''The search used is n-squared. TO DO: use a faster search
    that takes advantage of the fact that both the
    character_table and the subrange_iterator are sorted
    iterables of unique values.'''
    return tuple(
        map(
            lambda x: x if isint(x) else None,
            mapchain(
            subrange_iterator,
            partial(argswap(find), tuplemap(first, character_table)),
            tuple,
            first,
            ident)))

def character_chart_page_character_ord(
        character_table=CHARACTER_TABLE_STDOUT,
        page=0):
    return character_chart_character_ord(
        character_table=character_table_STDOUT,
        subrange_iterator=iter(range(
            128 * page, 128 * (1 + page))))
    
def character_chart_page(
        character_table=CHARACTER_TABLE_STDOUT,
        page=0):
    return tuple(
        mapchain(
            getitems(
                character_table,
                character_chart_page_character_ord(
                    character_table=character_table, page=page),
                default=('')),
            last,
            lambda s: SPACE if len(repr(s)) != 3 else s)
        )
    
def character_chart_page_print(page):
    print(*(2*HEX_DIGITS[:16]))
    for i in range(4):
        print(*page[i*32:(i+1)*32], end='')
        print('', '', i, '/', 1 + i)


