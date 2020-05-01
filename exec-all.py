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

# f = open('p:/exec-all.py');   exec(f.read());   f.close();   del(f)
# HISTORY
# 2018-09-25:   added characters.py
# 2018-07-12:   added import of stdout
# 2018-06-19:   set temp_path to full network path
# 2017-12-18:   Refactor, eliminate variables, added clean-up (del), begin to factor out path.
# 2017-11-17:   Released to //ad.sfwmd.gov/dfsroot/data/wsd/MOD/dparrish/My/Projects/LWCSIM/HOB/OBS/HOB/
# 2017-12:      modified

temp_path = '//ad.sfwmd.gov/dfsroot/data/wsd/MOD/dparrish/My/Code/Py/TP/' # 'p:/'
from sys import stderr, stdin, stdout
print('stderr: exec-all.py (STATUS): Attempting exec on contents of files...', file=stderr)
for temp_filename in map(lambda s: s + '.py', '''
        2500iterables
        2500iterators
        2500sequences
        3750sequences
        5000characters
        5000maths
        5000restore
        5000string
        7500files
        7500iterables
        7500string
        fun-prog
        triv00
        arith01
        maps
        core
        sets
        characters
        chtype
        ranges
        util-debug
        imports
        tuples
        search
        maths00
        iterables01
        iterables
        maths01
        generators02
        subs
        string
        sequences
        arith
        intervals
        values
        chnames
        dicts
        iteration
        lists
        deques
        arguments
        files
        tables
        fmt
        generators
        lines
        pops
        logic
        raster
        alternates
        dates
        deco
        clu
        '''.split()):
    with open(temp_path + temp_filename) as temp_f:
        print(
            'stderr: exec-all.py: loading and exec-ing:',
            '\n\t\t'.expandtabs(4),
            temp_f.name,
            sep='', end='', file=stderr)
        exec(temp_f.read())
        print(file=stderr)

del(temp_f, temp_filename, temp_path) # should delete all variables created within this script

