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

class files(tuple):
    '''Intended purpose: to enable using the with statement on
    tuples of files. Example:
            >>> with openw('t:/original') as f:
            ...     nul = f.write('as you wish\n')
            ...
            >>> with files((open('t:/original'), openw('t:/copy'))) as ff:
            ...     IN, OUT = range(2)
            ...     nul = ff[OUT].write(ff[IN].read())
            ...
            >>> tuple(map(lambda f: f.closed, ff))
            (True, True)
            >>> with open('t:/copy') as f:
            ...     f.read()
            ...
            'as you wish\n'    
    Reference: http://www.ironpythoninaction.com/magic-methods.html#
    context-managers-and-the-with-statement'''
    def __init__(self, iterable=(), keys=()):
        self = tuple(iterable)
        from io import IOBase
        assert all(mapchain(self, type, partial(argswap(issubclass), IOBase))), \
                'All items must be file-like objects (i.e., subclass of IOBase)'
    def __enter__(self):
        return self
    def close(self):
        unstar(fclose)(self)
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Close all files.'''
        self.close()
        return False

def fdump(filename):
    '''print-s the entire contents of the file specified by name.
    '''
    with open(filename) as f:
        print(f.read())

def fwords(file):
    '''Returns an iterator over the remaining words in a file.
    If the file position is at the middle of a word, the
    remaining part of that word counts as a word in this
    context.'''
    return flatt(map(towords, file))

def fcat(outfile=stdout, infilenames_iterable=(), quiet=True):
    '''Writes the entire contents of the files produced by the
    infilename_iterable to the outfile. The outfile may be a
    file open for writing or the name of a (typically new) file
    to be *OVERWRITTEN.*
    '''
    assert False, 'STATUS: IN PROGRESS'
    outfile = outfile if outfile == stdout else open(outfilename, 'w')
    for infilename in infilenames:
        write_return = outfile.write(freadentire(infilename))
        if not quiet:
            printerr('fcat (', write_return, '): ', infilename, sep=NULL)
    if outfile != stdout:
        outfile.close()

printn = partial(print, sep=NEWLINE)
printn.__doc__ = (
    'same as print, but with items separated by NEWLINE.')

def printbare(*args, sep='', end='', file=stdout):
    '''Same as print, but with different defaults.'''
    print(*args, sep=sep, end=end, file=file)

def fcharactermap(file):
    '''Returns a map that produces the characters of file The
    behavior of the return is affected by the file position,
    which may be manipulated after fcharactermap returns.
        DETAILS. The return produces an indefinite number of
    characters: the file position of the underlying file may be
    altered. HOWEVER, once EOF occurs, StopIteration is raised
    for each successive call to next, EVEN IF the corresponding
    file is (partially or fully) rewound. Analogy: walking back
    and forth toward and away from the edge of a cliff: as long
    as you don't go off the edge, you can continue to walk back
    and forth.'''
    #OLD return quota(map(fread, steady(file)), n=None, criterion=bool)
    while True:
        c = fread(file)
        if c:
            yield c
        else:
            return

def filestream(file, blocks=iter, parse=towords):
    '''Returns a map of the contents of the file. The default
    artuments assume that the file is organized into lines and
    that data elements are string literals separated by
    whitespace.
        The blocks optional argument is a function that takes
    file as its sole argument and returns a map of the file-s
    "blocks," which represent contiguous data elements. The
    default returns an iterator over the (text) file-s lines.
        The parse optional argument (a function) takes a block
    argument and returns an iterable of data elements
    represented by that block. The default returns a tuple of
    whitespace-separated "words."
       Example:
with open('p:/time-code-example.txt') as file:
    printbare(*filestream(
        file,
        blocks=lambda f: f.read(), # READ ENTIRE FILE
        parse=ident)) # SHOW FILE "AS-IS"

with open('p:/time-code-example.txt') as file:
    printbare(*filestream(
        file,
        parse=ident)) # SHOW FILE "AS-IS"

with open('p:/time-code-example.txt') as file:
    printbare(*filestream(
        file,
        parse=lambda line: map(
            lambda dig: ' one' if dig == '1' else
                ' zero' if dig == '0' else
                    '',
            tuple(line)))) # SHOW FILE "BENDER STYLE"
    '''
    return stream(blocks(file), parse=parse)

def makefilename(dev, dirs, nameparts, ext=''):
    '''Returns a filename formed by the concatenation of the str
    dev with the concatenation of the str-s in the iterable
    dirs, the concatenatoin of the str-s in nameparts, and the
    optional extension. Example:
            >>> makefilename('c:/', ('temp/', 'a/'), ('file', '-1'), '.txt')
            'c:/temp/a/file-1.txt'
    '''
    return dev + strcat(dirs) + strcat(nameparts) + ext

def makefilenames(devs, dirs, nameparts, exts):
    '''Multi-file version of makefilenames. Returns a map of the
    corresponding file names. Intended for use in producing
    systematic filenames that correspond in some way.  devs and
    exts are str iterables, dirs and nameparts are iterables of
    str iterables. Examle:
tuple(makefilenames(
    ('c:/',)*2,
    zip( # this is one way to get filenames at different levels
         # of the directory tree when part of the path is in
         # common.
        ('directory/',)*2,
        ('subdirectory/', '')),
    (
        ('two','-parts'),
        ('onepart',)),
    (
        '.txt',
        '.bin')))

    returns ('c:/directory/subdirectory/two-parts.txt',
            'c:/directory/onepart.bin')
        '''
    return map(unstar(makefilename), zip(devs, dirs, nameparts, exts))

def ziplines(iterable):
    '''Given an iterable of files, returns a zip object of the
    lines of the files. Useful for merging parallel lines from
    two or more files.'''
    return zip(*map(iter, iterable))

def fappend(fout, fin):
    fout.write(fin.read())

'''
def openw '''
openw = fopenw

def ffopen(filenames, modes=()):
    '''Returns a tuple where each element corresponds with those
    of the sequence filenames (arg 0). The value of each element
    of the return is either an open-ed file (if open was
    successful) of None (if unsuccessful). Each file is open-ed
    according to the sequence modes (arg 1).  If mode is not
    specified, or has zero length, 'r' is assumed.  If modes has
    at least one element, but has fewer than filenames, the
    modes for the remaining files will be the same as the last
    mode specified.  HISTORY 2018-09-10 previously returned a
    list; prevoiusly opened no more than len(modes); previously
    break-ed if open failed'''
    if not filenames:
        return ()
    lenf = len(filenames)
    if not modes:
        modes = ('r') * lenf
    shortfall = lenf - len(modes)
    if 0 < shortfall: # above logic guarantees 1 <= len(modes)
        modes = modes + (modes[-1],) * shortfall
    ff = [None] * lenf
    for i, (filename, mode) in enumerate(zip(filenames, modes)):
        try:
            f = open(filename, mode) # build list of files
            ff[i] = f
        except:
            pass
    return tuple(ff)

#TAGS   file dictionaries   file dictionary

def omdictoffilenames(modes, filenames):
    '''Returns a one-to-many dictionary for use with e.g.,
    ffopend. The modes produced by the modes iterable argument
    should correspond with the filenames produced by the
    filenames iterable argument.'''
    return omdict(zip(modes, filenames))

omdictoffiles = omdictoffilenames #DEPRECATED use omdictoffilenames

def ffopend(dictionary):
    '''Similar to ffopen, but takes a single dictionary argument
    (a one-to-many dictionary; see omdict) whose keys are the
    desired modes and whose values are tuples of filenames.'''
    d = {}
    for k in dictionary.keys():
        d.update({k: ffopen(dictionary[k], (k,))})
    return d

def ffopenderr(filename_dictionary, file_dictionary):
    d = {}
    for k in file_dictionary:
        d.update({k: tuplemap(second, filter(
            un(first),
            zip(file_dictionary[k], filename_dictionary[k])))})
    return d

def ffopenderrprint(filename_dictionary, file=stdout):
    dictprint(
        filename_dictionary,
        lambda t: print(
            *tuplemap(
                strcat,
                zip(
                    astuple('\t'.expandtabs()) * len(t),
                    t)),
            sep=eol()))

def ffclosed(dictionary):
    for k in dictionary.keys():
        for f in dictionary[k]:
            if f: # f could be None or file
                f.close()

###

def decofilesub(function):
    '''Deco File Subroutine. Originaly indended to be applied as
    a file decorator. The function argument is a function of an
    open file and other arguments. The inner function performs
    the function, then returns the file to its original
    position.'''
    def inner(f, *args, **kwargs):
        pos = f.tell()
        ret = function(f, *args, **kwargs)
        f.seek(pos)
        return ret
    return inner

def decoopend(function):
    '''"Deco Open Dee." Originally intended to be applied as a
    function decorator. The primary argument of function is a
    file dictionary (a one-to-many dictionay where keys are file
    open modes and the values are, tuples (or lists) of files).
    There is no restriction on the other arguments of the
    function: the signature is (d, *args, **kwargs). Returns a
    function where the primary argument is a *filename*
    dictionary (as opposed to a file dictionary).  Additionally,
    decoopend does the work of opening each file in the mode
    specified, calling the function, and closing the files
    afterwards.  The original function is called using the files
    indicated. Finally, the files are closed. See
    decoopdenexample for an example.
    '''
    def inner(filename_dictionary, *args, **kwargs):
        df = ffopend(filename_dictionary)
        printerr('decoopend: inner: df:', df)
        err = ffopenderr(filename_dictionary, df)
        if not omdictisempty(err):
            printerr('decoopend: inner:',
                'The following modes and filenames could not ' +
                ' be used to open files:')
            ffopenderrprint(
                ffopenderr(filename_dictionary, df),
                file=stderr)
        ret = function(df, *args, **kwargs)
        ffclosed(df)
        return ret
    return inner

@decoopend
def decoopendexample(file_dict):
    '''Copies the first 'r'-mode file to the first 'w'-mode file.'''
    file_dict['w'][0].write(file_dict['r'][0].read())

def fwriteall(file, string_iterator):
    '''write-s to file every string in the string_iterator.
    Returns the number of strings written (null strings cannot
    be written).'''
    return sum(mapchain(string_iterator, file.write, bool))

def fsplit(infile, directory, quiet=True, reset=rewind): # split file
    '''Splits a file line-wise into separate files. The file is
    reset according to the reset function (this allows for
    header lines to be skipped in an external process). Leading
    whitespace is ignored. The first whitespace-delimited
    substring is a key. Lines of the same key are written to a
    file of the same name, in the directory specified (the
    directory should end with a path separator, e.g. "/"). The
    lines are written in the order encountered in the infile.
    Leading whitespace, key, and whitespace immediately after
    the key will be absent from the files created.'''
    for key in frozenset(mapchain(rewind(infile), words, first)):
        if not quiet:
            printerr('fsplit: key:', key)
        with openw(directory + key) as outfile:
            for item in filteriterables(mapchain(
                    reset(infile), words, iter,
                    lambda r: tuple(flat(next(r) == key, r)))):
                print(*item, file=outfile)

def fsplitordered(
            infile,
            outdirectory,
            key=lambda line: first(words(line)),
            unkey=compose(str.lstrip, strtail),
            quiet=True,
            reset=rewind):
    '''Similar to fsplit, but with the simplifying ASSUMPTION
    that the lines are sorted in order by key (each of which
    becomes the filename of each partial output). unkey is a
    function of line that defines what will be output; the
    default is to strip off the first word and whitespace
    separating that word from the rest of the line. Returns a
    tuple of keys found, in the order they are found; keys may
    appear multiple times if lines of the infile are not sorted
    by key.'''
    keylist = []
    for section in sections(reset(infile), match=
            lambda head, other: key(head) == key(other)):
        head = next(section)
        k = key(head)
        keylist.append(k)
        if not quiet:
            printerr('fsplitordered: section key:', k)
        with openw(outdirectory + k) as outfile:
            for line in chain((head,), section):
                printbare(unkey(line), file=outfile)
    return tuple(keylist)

'''
    for k in frozenset(map(key, rewind(infile))):
        with openw(dirout + k) as fo:
            for line in rewind(infile):
                kk = key(towords(line))
                if kk == k:
                    fo.write(line)
'''
@decoopend
def filemap(
    files,
    load=(filestream,),
    function=compose(
        partial(str.format, '{0}'),
        lambda *x: 0),
    write=fwriteall):
    '''Reads values from each of the r-mode files specified in
    the filename_dict. Values are read according to the
    functions in the sequence load (typically a tuple or list;
    one funciton per r-mode file---values will be recycled if
    necessary to obtain the number of r-mode files).  Computes
    the corresponding sequence of values with function---a
    function of a number of variables equal to the number of
    r-mode files in filename_dict; the function should return a
    string.  Writes the computed values to the first w-mode file
    specified in the filename dictionary.
    Example:
    mfu2drelmake(
    {'w': ('t:/stuff',), 'r': ('t:/trash', 't:/junk')},
    #load=(vectorstream, partial(vectorstream, function=int)),
    function=lambda x, y: x + y)
    '''
    write(
        first(files['w']),
        map(function, *zipapply(
                recycle(load),
                files['r'])))

def decoopen(function):
    '''"Deco Open." Originally intended to be applied as a
    function decorator. The function argument takes two
    tuples of files and other arguments (ffin, ffout, *args,
    **kwargs). Deco Open returns a function of two strings and other
    arguments (stin, stout, *args, **kwargs). In the return-ed
    function, The stin and stout
    arguments are used to open the corresponding files in 'r'
    and 'w' modes when function return-ed by Deco Open is called. The
    stin and stout arguments specify files separated by the
    initial character of the respective strings, e.g.,
    ' /home/guest/file1 /home/guest/file2' might specify file1 and
    file2 in the guest user's directory. The original function
    is called using the files indicated. Finally, the files
    are closed. See decoopenexample for an example.
    WHEN APPLYING THE RETURNED FUNCTION, if "other arguments" are applied but no output file is
    specified, it will be necessary to have a placeholder for
    the outfiles, e.g., function(" infile" , " ", arg2) the HISTORY
    2018-04-26 modified to return the value of function.'''
    def dofileerr(direction, string):
        printerr(' decoopen: Formation of ', direction,
                ' file names and files from "', string,
                '" failed.', sep='')
    def inner(stin, stout, *args, **kwargs):
        printerr('decoopen: inner: args:', args)
        try:
            splitins = strsplit0(stin)
            printerr('decoopen: inner: infile names:', *splitins, sep=NEWLINE)
        except:
            pass
        try:
            ffin = tuple(map(open,  splitins))
        except:
            dofileerr('input', stin); return
        try:
            splitouts = strsplit0(stout)
            printerr('decoopen: inner: outfile names:', *splitouts, sep=NEWLINE)
        except:
            pass
        try:
            ffout = tuple(map(fopenw, strsplit0(stout)))
        except:
            dofileerr('output', stout); return
        printerr('decoopen: inner: args:', args)
        printerr('decoopen: inner: kwargs:', kwargs)
        ret = function(ffin, ffout, *args, **kwargs)
        map(lambda f: f.close(), chain(ffin, ffout))
        return ret
    return inner

'''
def fntplfintplfoutargkwargtofnstrstrargkwarg # alias
'''
fntplfintplfoutargkwargtofnstrstrargkwarg = decoopen # alias

def decodo(function):
    '''Deco Do. Originally intended to be applied as a decoroator outside of
    decoopen, e.g.:
    .
    @decodo
    @decoopen
    def function(st0, st1):<rest of funcdef>
    .
    Given a function of one or more strings, returns a function
    of a single, compound string that will be split into two
    strings before passing into the original function of two
    strings.
    '''
    def inner(st):
        #stin, stout = strsplit0(st)
        #function(stin, stout)
        st = strsplit0(st)
        printerr('(STATUS)', 'decodo: st:', st)
        function(*st)
    return inner

@decoopen
def decoopenexample(ffin, ffout, sep=''):
    '''Example usage of decoopen. The present decorated function
    takes a string representing input files, a string
    representing a single output file, and an optional
    separator. Copies of the input files are written to the new
    output file. Each copy is optionally preceeded by a copy of
    the string sep (it is anticipated that the final character
    of sep will be newline). Example:
    # FILE trash-1
    this is a test
    # FILE trash-2
    this is another test
    decoopenexample(' t:/trash-1 t:/trash-2', ' t:/trash-o',
    sep='--------\n') # writes the following to trash-o:
    --------
    this is a test
    --------
    this is another test
    '''
    for f in ffin:
        ffout[0].write(sep)
        for line in iter(f.readline, ''):
            ffout[0].write(line)

def _load(filename):
    with open(filename) as f:
        return f.read()

def load(filename, xdef=''):
    '''Returns from the file specified by filename the *text*
    that belongs to the xdef (either a classdef or a funcdef)
    specified, assuming both corresponding file and xdef exist.
    The corresponding xdef should be nicely formatted; the
    procedure for identifying xdef-s is not absolutely robust.
    The following pattern is assumed to match a funcdef:
    ^def\s+string\s*([^\n]\n
    i.e., beginning of line, 'def', whitespace, NAME, left
    parenthesis, any non-end-of-line markers, end-of-line
    marker. Similarly for classdefs:
    ^class\s+string\s*:[^\n]\n
    FUTURE: recognize more complex classdefs.
    '''
    def defname(s):
        'Returns the name of the function in a def statement'
        if not line.startswith('def'):
            return '' # we're interested only in def-s at the top level
        if not line.split()[0] == 'def':
            return '' # we don't want lines beginning with defa, defb, etc.
        l = line.partition('(') # == ['def' + string, '', ''] or ['def' + string, '(', string]
        if l[1] != '(':
            return ''
        l = l[0].split() # == ['def' \[, string\]* ]
        if len(l) < 2:
            return ''
        # l == ['def', string] or ['def', string, string] or ...
        return l[1] # == string == function name
    def classname(s):
        ''
        if not line.startswith('class'):
            return '' # we're interested only in def-s at the top level
        if not line.split()[0] == 'class':
            return '' # we don't want lines beginning with clases, classify, etc.
        l = line.partition(':') # == ['class' + string, '', ''] or ['class' + string, ':', string]
        if l[1] != ':':
            return ''
        l = l[0].split() # == ['class' \[, string\]* ]
        if len(l) < 2:
            return ''
        # l == ['class' \[, string\]+]
        return l[1] # == string == function name
    def continuation(line):
        return bool(line) and (line[0] in {'\t', ' '})
    if not xdef: # xdef not specified---return entire file text
        return _load(filename)
    dlines = []
    with open(filename) as f:
        lines = iter(f)
        for line in lines:
            if (classname(line) == xdef) or (defname(line) == xdef):
                dlines.append(line) # first line of def
                for line in lines:
                    if not continuation(line):
                        break
                    dlines.append(line)
                break
    return ''.join(dlines)

def fhead(filename, n=10):
    '''print-s (to stdout) the first n lines of the file
    specified by filename. HISTORY 2018-12-14: completely
    rewritten.'''
    with open(filename) as infile:
        for line in quotan(infile, n):
            print(line, end='')

def genfcolumn(f, n=0):
    for line in genlinesfromfile(f):
        yield wordn(line, n)

def fcolumnprint(f, n=0):
    '''prints the n-th word of each of the lines in file f, from
    the current file position onward'''
    for word in genfcolumn(f, n):
        print(word)

def freadnat(f, at, n):
    return fread(freset(f, pos=at), n)

funread = decononadvancingfilefunction(fread)
'''Returns the next n characters read from file. The final
file position is restored to the initial file position.'''

eofapproached = compose(un(bool), funread)
'''Returns a bool indicating whether there is any more data in
file f open for reading'''

def fclose(*files):
    '''HISTORY 2018-05-10: now accepts any number of files.'''
    waste(map(lambda f: f.close(), files))

def fileiter(filenames):
    '''Given an iterable of file names, yield-s files, open for
    reading text. When yield-ed, each file is set at its initial
    position.  It is intended that the iterators produced from
    this generator are fully exhausted: each file is closed
    after it is yielded.'''
    for filename in filenames:
        f = open(filename)
        yield f
        f.close()

def funwordskip(file, iswordch=isgraph):
    '''"eff un-word skip" Skip non-word characters in file f.
    Returns the last character read, or the null string, if EOF
    occurs. File position is set to read the REST of the word
    whose first character is encountered here.'''
    while True:
        c = fread(file)
        if c == '' or iswordch(c):
            return c

def fgetrestofword(f):
    '''Advances file f *IN PLACE*. read-s the next contiguous
    sequence of graphic characters from f, as well as any single
    non-graphic character that follws (which should be present
    if EOF does not occur first) immediately after the current
    word. Returns the sequence as a string.'''
    lst = [fread(f)]
    while isgraph(last(lst)):
        lst.append(fread(f))
    return ''.join(lst)

def fgetword(f):
    while True:
        w = fgetrestofword(f)
        if not w or isgraph(w[-1]): # EOF
            return w
        if 1 < len(w):
            return w[:-1]


def ffproc(filenames, func, retrieve):
    '''Process Files. Open files specified by the list filenames, read data
    from each, according to the retrieve function, and send data, along with
    file handles, to function func for optional processing and possible
    alteration of the file position; repeat until func returns False or
    equivalent.  FUTURE: handle a list of retrieve functions, each particular
    to its own file.'''
    printerr('ffproc:','filenames:', filenames)
    printerr('ffproc:','type(filenames):', type(filenames))
    f = list(map(lambda s: open(s), filenames))
    fret = True
    printerr('ffproc:')
    while fret:
        t = retrieve(f) # read data from each file
        fret = func(t, f) # call func, which might alter file pos
    map(lambda x: x.close(), f) # close all files

#### Writing

def fwriteallsep(f, string_iterator, sep=' ', truesep=False):
    '''Similar to fwriteall, but prepends each item output with
    sep. Also similar to print.'''
    strings = flat(*zip(iter(constant(sep), ''), string_iterator))
    if truesep: # remove the first separator, if there is one
        next(strings, NoMore)
    return fwriteall(f, strings)

def writeskip(f, lst=[''], skip=0):
    '''write-s the strings of the simple list lst to file f, beginning at the
    current file position and such that there are skip bytes between items.
    Intended for use in writing to multidimensional arrays. returns the number
    of bytes written.'''
    if f.mode != 'wb':
        return 0
    if not len(lst):
        return 0
    n = 0
    ipos = f.tell()
    for ndex, item in enumerate(lst):
        f.seek(ipos + ndex * skip)
        n = n + f.write(item)
    return n

def fcharacterset(file, seek=rewind):
    '''returns a frozenset of the characters found in the tail
    of the file.  The seek argument controls how much of file is
    used to build the character set. By default, the entire file
    is used.  Alternatively, a function may be specified which
    returns the file (optionally after mutating the file
    position). Common values for seek might include ident (no
    mutation of file position) and compose(rest, rewind)
    (rewind, then skip first line, assuming a text file).

    HISTORY:

            2019-07-10:

                    formerly returned a set rather than a
                    frozenset.

                    formerly read the entire file before
                    computing the character set. now reads one
                    character at a time.
    '''
    seek(file);   return frozenset(fcharactermap(file))

def fcharacterset(file, seek=rewind):
    cs = fcharacterset(file, seek=seek)

def fworditer(f):
    return iter(partial(fgetword, f), '')

def freadeveryword(f):
    return tuple(f.read().split())

def loadvector(f, function=float):
    '''Returns a map of values represented by words in the text
    file f. Reads the entire contents of the file past the
    initial file position. FUTURE: lazily read the file, limit
    number of words read, etc.'''
    return map(function, f.read().split())

def fpaginate(infile, files, match=alwaysTrue, assess=constant(48)):
    '''Beginning at the current file position of file infile,
    copies sections of infile to a sequence of files specified
    by applying the files function with the seciton number
    (beginning from zero). The match and assess functions are
    supplied to the sections function, and determine page
    breaks.'''
    for pageno, page in enumerate(sections(infile, match=match, assess=assess)):
        with openw(files(pageno)) as fo:
            print(*page, sep='', end='', file=fo)

@decoopend
def fmultiwriteall(file_dictionary, *string_iterables):
    '''write-s the strings produced by each string_iterable to
    the corresponding w-mode file in the file_dictionary.'''
    waste(map(unstar(fwriteall), zip(file_dictionary['w'], string_iterables)))

