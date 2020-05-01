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

# RENAMED FROM py.py ON 2019-01-11
#
# THIS FILE SOON TO BE SUPERSEDED (USING AS A TEST CASE TO
# BECOME MORE FAMILIAR WITH GITHUB).

RESTORE = \
'''"""(ENTER print(restore) TO SEE THIS MORE CLEARLY).

ENTERING exec(restore) FROM THE >>> PROMPT SHOULD DELETE ALL
NON-DUNDER NAMES (NAMES THAT DO NOT BOTH BEGIN AND END WITH
DOUBLE UNDERSCORE) EXCEPT restore.
"""
for name in dir():
    part = name.partition('__')
    if name in ('restore', 'name', 'part'):
        pass # name is being used in-loop: don't delete
    elif part[0]: # name does not begin with '__'
        exec('del ' + name)
    elif part[1] == '__': # name begins with '__'
        part = ''.join(reversed(part[2])).partition('__')
        if part[0]: # name does not end with '__'
            exec('del ' + name)
    else:
        pass

del name, part
####678
#f = open('p:/exec-all.py');   exec(f.read());   f.close();   del(f)
'''
