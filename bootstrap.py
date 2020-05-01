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

#                       SYSTEM BOOTSTRAP
#
#
# DESIGN
#
# Edit TEMP_PATH to indicate the directory where the files of
# this system are stored.
#
# Add or remove any files from the long list of py files. The
# system is designed so that files loaded later may depend on
# the objects that are created by exec-ing the files loaded
# earlier.
#
# Bootstrap the system from the >>> prompt with on *nix or
# Windows:
# 
# f = open('~/CODE/Py/3/TP/bootstrap.py'); exec(f.read()); f.close(); del(f)
# f=open('p:/bootstrap.py'); exec(f.read()); f.close(); del(f)
#
# **** NOTE **** Previous attempts to bootstrap with e.g.:
#
#       with open('p:/bootstrap.py') as f:
#           exec(f.read())
#
#       del f
#
# have **** FAILED. ****
#
#
# HISTORY
#
# 2018-09-25:   added characters.py
# 2018-07-12:   added import of stdout
# 2017-12-18:   Refactor, eliminate variables, added clean-up
#               (del), begin to factor out path.
# 2017-12:      modified

STDERR_PREFIX = '2>  '

TEMP_PATH = 'p:/'
from sys import stderr, stdin, stdout
print(
    STDERR_PREFIX,
    STDERR_PREFIX + 'bootstrap.py: Attempting exec on contents of files...',
    STDERR_PREFIX,
    sep='\n', file=stderr)
for TEMP_FILENAME in tuple(map(lambda filename: filename + '.py', '''
        0312imports

        0156fun-prog
        0312arith
        0312characters
        0312deques
        0312integers
        0312strings
        0312triv
        0312tuples
        0390filters
        0469ranges
        0547strings
        0625files
        0625iterables
        0625maths
        0625fun-prog
        0938maths
        1250files
        1562string
        2500iterators
        2500iterables
        2500sequences
        3750sequences
        5000maths
        5000restore
        5000string
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
        8750bytes
        8750algebra
        8750hex
        9375files
        '''.split())):
    TEMP_FULLNAME = TEMP_PATH + TEMP_FILENAME
    print(STDERR_PREFIX + TEMP_FULLNAME, file=stderr)
    with open(TEMP_PATH + TEMP_FILENAME) as TEMP_FILE:
        print(STDERR_PREFIX, file=stderr)
        print(
            STDERR_PREFIX +
                    'bootstrap.py: Loading and exec-ing:',
            (STDERR_PREFIX + '\t' + TEMP_FILE.name).expandtabs(4),
            sep='\n', file=stderr)
        TEMP_TXT = TEMP_FILE.read()
        #print(TEMP_TXT, file=stderr)
        exec(TEMP_TXT)

del(TEMP_FILE, TEMP_FILENAME, TEMP_FULLNAME, TEMP_PATH, TEMP_TXT) # should delete all variables created within this script

print('''
###############################################################

                         TEXT PROCESSOR

                       Copyright (C) 2018*
                       D. Michael Parrish


         Once you have written a hundred or a thousand
         words that discuss a problem,   you are ready
         to solve it.
                           ---Charles H. "Chuck" Moore

###############################################################''', file=stderr)


"""
"""
