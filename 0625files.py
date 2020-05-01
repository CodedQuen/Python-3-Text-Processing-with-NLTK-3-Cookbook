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

def loadentireaslines(filename):
    '''returns the entire contents of the file, specified by
    filename, as a tuple of lines.'''
    with open(filename) as f:
        return tuple(f)

def apply(function, *args_and_kwargs):
    assert False, 'STATUS: In Progress'
    args = args_and_kwargs
    function(*args_and)

def halffapply(filename, function, binary=False):
    '''returns a function of no variables that, when called,
    opens the file specified by filename with the mode specified
    by binary, applies function (a function of one file
    variable, corresponding to filename), and returns the function
    result.  Internally, the file mode is either "rb" or "r".
    '''
    def unevaluated():
        with open(filename, 'rb' if binary else 'r') as file:
            return function(file)
    return unevaluated

def fapply(filename, function, binary=False):
    '''returns the result of function, which is applied to the
    file whose name and mode is specified. Internally, the file
    mode is either "rb" or "r".
    '''
    with open(filename, 'rb' if binary else 'r') as file:
        return function(file)

def halffmap(function, filenames, binary=False):
    '''map-s files, specified by the iterable of filenames.
    Internally, files are opened in read-binary or read-text
    mode according to the binary argument.
    '''
    return map(
        partial(
            halffapply,
            function=function,
            binary=binary),
        filenames)

def fmap(function, filenames, binary=False):
    '''map-s files, specified by the iterable of filenames.
    Internally, files are opened in read-binary or read-text
    mode according to the binary argument.
    '''
    return map(
        partial(
            fapply,
            function=function,
            binary=binary),
        filenames)

def fbytes(file):
    '''returns an iterator through the remaining bytes of the
    file open for binary reading, "rb".
    '''
    return iter(partial(fread, file), b'')

def freadentire(filename): ###
    '''Return entire contents of file specified by the string
    filename. History--- 2017-12-28: changed argument name;
    changed argument to positional argument.'''
    with open(filename) as f:
        return f.read()

def opena(filename): #TAGS append file
    return open(filename, 'a')

def fopenw(filename): #TAGS write file
    return open(filename, 'w')

def fread(file, n=1): ###
    '''Wrapper for file.read(n)'''
    return file.read(n)

def freset(file, position=0): ###
    '''Sets (absolute) file position. Returns the file.'''
    file.seek(position);   return file

def rewind(file): #TAGS seek
    '''Sets file position to beginning. Returns the file.'''
    return freset(file)

def fread_previous(f, n=1024): ###
    '''Reads from file f the previous n *characters* or the
    number which occur before the current file position, if
    there are fewer than n. Restores f to original position.
    Reminder: multiple *bytes* may form the end-of-line
    marker.'''
    pos  = f.tell()
    newpos = max(0, p - n)
    f.seek(newpos)
    ret = f.read(pos - newpos)
    f.seek(pos)
    return ret

def decononadvancingfilefunction(file_function): ###
    '''Intended as a function decorator. Given a function whose
    first argument is a file, returns a function that has the
    same effect, except that the position of the file in
    question is restored to its initial position upon return.'''
    def nonadvancingfilefunction(file, *args, **kwargs):
        pos = file.tell()
        ret = file_function(file, *args, **kwargs)
        file.seek(pos)
        return ret
    return nonadvancingfilefunction

