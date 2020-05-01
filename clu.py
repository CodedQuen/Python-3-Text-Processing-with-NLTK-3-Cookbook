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
### COMMAND LINE UTILITIES
''' Usage:
            u:\pyu COMMANDNAME "* [$infile0[$infile1[...]]
            [$outfile0[$outfile1[...]] [arg2 [arg3 [...]]]]]*
            [key0 value0 [key1 value1]]"

    Example:

            u:pyu middled "* r filename** line 42 lines 16"
'''
def decoclu(function):
    '''Given a function of a tuple of input (read-mode) text
    files, a tuple of output (write-mode) text files, zero or
    more positional arguments, and zero or more keyword
    arguments, returns a function of a string. The actual
    argument of the call of such a function has the form:
    {sep-outer}{minor-sep}{sepouter}
    '''
    return fnstrstofnstr(fnargkwargtofnstrs(decoopen(function)))

decoklu = lambda function: fnfndargkwatofnstrstr(decoopend(function))

@decoclu
def catheader(ffin, ffout, out_directory):
    '''Creates modified copies of files listed in ffin[0] in
    out_directory. Each copy will contain the contents of
    ffin[1] at the beginning.'''
    header = ffin[1].read()
    for filename in freadeveryword(ffin[0]):
        with open(out_directory + filename, 'w') as fo:
            fo.write(header)
            with open(filename) as fi:
                fo.write(fi.read())

def _cat(ffin, ffout):
    ffout = ffout if ffout else (stdout,)
    PRINT = partial(printbare, file=first(ffout))
    for fin in ffin:
        for line in fin:
            PRINT(line)

#TODO MAKE ~cat~, WHICH COPIES CONTENTS OF ONE FILE TO ANOTHER
def catlist(infilenames, outfilename):
    with openw(outfilename) as fo:
        for infilename in infilenames:
            with open(infilename) as fi: #~cat~
                for line in fi:          #~cat~
                    fo.write(line)       #~cat~

cat = decoclu(_cat)

@decoklu
def catd(file_dictionary):
    _cat(
        file_dictionary['r'],
        () if 'w' not in file_dictionary else file_dictionary['w'])

@decoclu
def copy(ffin, ffout):
    '''print-s the contents of the list of files stored in ffin[0].'''
    print(*map(freadentire, strsplit(ffin[0].read())), sep='')

@decoclu
def head(ffin, ffout, lines='1'):
    '''print-s the first int(lines) lines of the first file in
    the ffin tuple'''
    print(*quota(lineiter(ffin[0]), int(lines)), sep='')

def _tail(ffin, ffout, lines=1):
    '''print-s the last int(lines) lines of the first file in
    the ffin tuple'''
    print(*lastitem(running(lineiter(ffin[0]), int(lines))), sep='')

tail = decoclu(_tail)

@decoklu
def taild(file_dictionary, lines=1):
    _tail(file_dictionary['r'], None, lines=lines)

def _middle(ffin, ffout, line='1', lines='1'):
    '''print-s the int(lines) lines of the first file in
    the ffin tuple, beginning with line int(line).'''
    skip(iter(ffin[0]), int(line) - 1)
    print(*nextlines((ffin[0]), int(lines)), sep='', end='')

middle = decoclu(_middle)

@decoklu
def middled(file_dictionary, line=1, lines=1):
    _middle(file_dictionary['r'], None, line=line, lines=lines)

@decoclu
def lineindexwrite(ffin, ffout):
    '''Intended to be called from the command line. Usage:
    py.exe run.py lineindexwrite "infile outfile" spaces in
    filenames not handled. This seems to run very slowly. For
    files of manageable size, perhaps reading entire file in
    binary will speed up.'''
    waste(mapchain(linepositions(ffin[0]), str, strasline, ffout[0].write))

@decoclu
def tablesplitcolumns(ffin, ffout, *outfilenames, path='', prefix='', suffix='', time=''):
    printerr('tablesplitcolumns:')
    from time import time
    for i, outfilename in enumerate(outfilenames):
        print(i, outfilename)
        t = time()
        with open(path + prefix + outfilename + suffix, "w") as fo:
            print(
                    *tablecolumn(
                    map(strsplit,
                            lineiter(rewind(ffin[0])),
                        ),
                    i),
                sep='\n',
                file=fo)
        print(time() - t, 'seconds.')

@decoclu
def tableextractcolumn(ffin, ffout, ncol):
    print(*mapchain(iter(ffin[0]),
            strsplit, partial(member, index=int(ncol))),
            sep='\n')

def _hcat(ffin, ffout, sep=' '):
    '''Concatenate columns of text found in the input files.
    Separate columns by sep.'''
    fo = stdout if not ffout else ffout[0]
    for line in mapchain(
            ziplines(ffin),
            lambda tpl: map(str.strip, tpl),
            sep.join):
        print(line, file=fo)

hcat = decoclu(_hcat)

@decoklu
def hcatd(file_dictionary, sep=SPACE):
    _hcat(file_dictionary['r'], file_dictionary['w'], sep=sep)

@decoclu
def dayspermonthgreg(placeholder_tuple, ffout, firstyear, lastyear):
    '''Given a tuple (not used, can be empty), a tuple of output
    files (can be empty; if not, only first one is used), and
    two strings (firstyear and lastyear), each of which are
    convertible to int-s that represent Gregorian Years, writes
    a table of number of days per month to ffout[0] (or stdout
    if ffout is empty). The table has three columns: year,
    month, and number of days; in that order. Example
    command-line call:
            u:\pyu dayspermonthgreg "* $ $outfile 1900 1900*"
    '''
    y0, y1 = int(firstyear), int(lastyear)
    print(
        *mapchain(
            flat(*map(
                lambda y: zip(
                    steady(y),
                    range1(12),
                    dayseachmonthgreg(isyearleapgreg(y))),
                range(y0, 1 + y1))), # `map` of `YYYY, MM, #Days`
            partial(map, str),
            partial(strcat, sep=' ')),
        file=stdout if not ffout else ffout[0],
        sep=eol())

@decoclu
def dos2unix(ffin, ffout, fnout):
    with open(fnout, mode='wb') as fout:
        for line in ffin[0]:
            fout.write(
                bytes(line.strip(), 'ascii') + bytes((10,)))
