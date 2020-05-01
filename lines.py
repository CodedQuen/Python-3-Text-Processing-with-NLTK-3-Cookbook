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
# LINES: Definitions related to extracting lines of text from files
# Definition:
#       a line is a string having exactly one newline character;
#       the newline character is the final character of the string.



'''
def freadeveryline(file) #DELETED USE tuple(file)
'''

def fread_previous_line(f, n=1024):
    '''Returns the line found before the current position of
    file f. On return, the file position of f is set *IN PLACE*
    just after the line returned; at the beginning of file if
    there was no previous line.'''
    pos  = f.tell()
    newpos = max(0, pos - n)
    f.seek(newpos)
    prevline = f.readline()
    if pos < f.tell(): # there is no previous line
        rewind(f)
        return ''
    while f.tell() < pos:
        psave = f.tell()
        nextline = f.readline()
        if pos < f.tell():
            f.seek(psave)
            break
        prevline = nextline
    return prevline

def pulseeol(period): #TAGS text EOL line breaks format
    return pulse(period, lambda flag: NEWLINE if flag else NULL)

def eol(): ###
    return '\n'

def linenumbers(lines):
    return map(first, enumerate(lines))

def linesnonblank(lines):
    return filter(lambda s: 1 < len(s), filter(None, lines))

def linesnonindented(lines):
    return filter(lambda s: isgraph(s[0]), linesnonblank(lines))

def linebare(string, stripchar=None):
    '''Function version of str.rstrip. HISTORY 2018-05-10:
    changed to do str.rstrip rather than str.strip, added
    stripchar kwa. Example:
            >>> linebare('this\\nis\\na\\nmultiline\\nrecord\\n\\n\\n')
            'this\\nis\\na\\nmultiline\\nrecord'
    '''
    return string.rstrip(stripchar)

def PLACEHOLDER(): # def printlines
    pass
printlines = partial(print, sep='', end='')



strasline = line #DEPRECATED use line

def linesplit(line, n=1):
    'Alias for towordsn'
    return towordsn(line, n)

'''
linescat('line 1\n', 'line 2\n', 'line 3\n', sep='|')
'''

def linescat(*lines, sep=' ', stripchar=eol()):
    '''Each element of Returns the lines as a singe line consisting of the
    contents of lines, stripped of intermediate end-of-line
    markers. The end-of-line marker on the final lines argument,
    if present, is preserved. HISTORY: changed primary argument
    to a starred argument. Example:
            >>> linescat('line 1\\n', 'line 2\\n', 'line 3\\n', sep='|')
            'line 1|line 2|line 3\n'
            >>> linescat(
                'multiline record part 1\\nmultiline record part 2\\n',
                'record 2\\n', sep='|')
            'multiline record part 1\nmultiline record part 2|record 2\n'
    '''
    assert all(map(partial(argswap(isinstance), str), lines)), \
            'Not all elements of lines are strings.'
    return sep.join(map(linebare, lines)) + eol()

def lineiter(f): ###
    '''Returns an iterator over the lines of f. Raises
    StopIteration after exhaustion.'''
    return iter(f)

def linereiterator(f, memory_size): # tags: lines file text reiterator
    '''Returns a reiterator over the file open for reading
    specified by the f argument. The reiterator will store up to
    memory_size rows of the file. The initial position of the
    iterator corresponds with the initial position of the
    file.'''
    return reiterator(iter(f), memory_size=memory_size)

def freadline(f): ###
    '''functional version of file.readline.'''
    return f.readline()

def freadlines(file, n=1):
    '''Returns a tuple containing the next n lines (or all
    remaining lines, if lines there are fewer than n remaining)
    of the file.'''
    return tuple(quotan(file, n))

def nextlines(file, n=1):
    '''Returns a map of the lesser of the next n lines of file,
    or the number of lines remaining, whichever is least.
        DETAILS. Setting n=None will eliminate the line count
    limitation. This at first seems to defeat the purpose of the
    function, however it might be applicable when specifying
    defaulg behavior elsewhere---see tablekeysfromfile, for
    example.'''
    return quota(iter(file), n=n, criterion=ident)

def remaininglines(f): ### HOW TO ENSURE FILE IS CLOSED WHEN, E.G., DON'T ACTUALLY NEED ALL LINES
    '''yield-s each line of f'''
    while True:
        line = f.readline()
        if not line:
            break
        yield line
    f.close()

def firstwordofeveryremainingline(f):
    return map(strfirstword, remaininglines(f))

def lineskip(f): ###
    '''If possible, skips to the next line of file f open for
    reading. Returns 1 if an end-of-line marker was read before
    EOF; 0 if EOF occurs before any characters are read; -1 if
    characters are read, but EOF occurs before an end-of-line
    marker is found.'''
    lin = f.readline()
    return 0 if not lin else 1 if (lin[-1] == '\n') else -1

def linecount(f):
    '''Returns a duple containing the number of end-of-line
    markers beyond the initial position of file f and a flag
    (int) indicating whether characters occur after the
    last end-of-line marker. If characters past the last
    end-of-line marker count as a line, the sum of the values in
    the duple is the line count. If not, the first item of the
    duple is the line count.'''
    i, k = 1, -1
    while i > 0:
        k = k + 1
        i = lineskip(f)
    # i < 1
    if i:
        return k, 1
    return k, 0

def linecounttest(st):
    with open(st) as f:
        print(linecount(f))

def lineskipn(f, n=1): #.#
    nls = 0 # number of line skipped
    while n:
        n -= 1
        if lineskip(f) < 1:
            return nls
        nls += 1

def linegoto(f, n=0):
    '''Set file position to beginning of line n, where line 0 is
    the first line,if possible.  Normally returns the number of
    end-of-line makers read since the beginning of the file
    (typically interpreted as line number). When EOF occurs
    before the requested number of lines has been reached,
    returns a negative integer whose absolute value represents
    the file position (line number).  If the user considers the
    EOF condition to be equivalent to end-of-line, the line
    count is equal to the absolute value of the return.'''
    m = 0
    rewind(f)
    for i in range(n):
        lc = lineskip(f) # lc: line count
        if not lc:
            return m
        if lc < 0:
            return -m - 1
        m += 1
    return m

# LINES

def linesextract(fin, fout, nlines):
    '''Read up to nlines lines from fin; write them to fout.'''
    return count(map(fout.write, quota(iter(fin), nlines)))

def linesskip(lstf):
    lst = []
    for f in lstf:
        lst.append(lineskip(f))
    return lst

def linesread(flst):
    '''Perform readline for each file in flst; return a corresponding list of
    strings.'''
    llst = []
    for f in flst:
        llst.append(f.readline())
    return llst

def linesskipc(lstf, tf):
    '''Conditional Line Skip. Advance position of the files in lstf past the
    next newline, provided the corresponding element of tf evaluates to True.'''

    info = zip(lstf, tf)
    lst = []
    for i in info:
        if i[1]:
            lst.append(i[0])
    linesskip(lst)

def linepositions(f):
    '''Advances file f *IN PLACE*. Given a file, returns an
    iterator over the file positions corresponding to the
    beginnings of lines. Data after the last end-of-line marker
    is ignored. The initial position of the file is assumed to
    correspond with the beginning of a line.'''
    return chain(astuple(f.tell()), allbutlast(map(fofnonetofofany(f.tell), lineiter(f))))

def lineindex(f):
    return mapchain(iter(f.readline, ''), constant(f), lambda f: f.tell())

def partiallineindex(f, line_numbers):
    i, l = 0, []
    for n in line_numbers:
        while i < n:
            f.readline()
            i += 1
        l.append((i, f.tell()))
    return dict(l)

@decoopen
def lineindexread(ffin, ffout):
    '''Reads the entirefile '''
    return tuple(map(int, fworditer(ffin[0])))

def lineproc(filenames, func):
    ffproc(filenames, func, linesread)

def linefind(f, func=bool):
    '''Advances f to the line where func returns True. Can be
    used to find comment lines, etc. Returns True on success,
    False on failure. Data found between the initial file
    position and the first end-of-line marker is considered to
    be a line'''
    pos = f.tell()
    while True:
        line = f.readline()
        if not line:
            break
        if func(line):
            f.seek(pos)
            return True
        pos = f.tell()
    return False

