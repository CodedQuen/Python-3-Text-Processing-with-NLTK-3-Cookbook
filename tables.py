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
'''Tables
Properties of tables:
    stored as text files.
    one line per record.
    a row is a tuple of items, each item corresponds to a cell
    of that row of the table.
'''

def tablerowiter(lines, splitfunc=towords):
    '''Given an iterator of lines, yields corresponding tuples
    of "cells" of text.'''
    for line in lines:
        yield splitfunc(line)

def tablerowsoriginal(rows, key):
    '''yields the non-duplicate rows of where rows have the same
    key, the first one is yielded.'''
    orig = set()
    for row in rows:
        k = key(row)
        if k not in orig:
            orig.add(k)
            yield row

def tablecolumn(rows, n=0):
    '''Given an iterator over rows (tuples of items) of a table,
    yield-s the n-th item of each.'''
    for row in rows:
        yield row[n]

def tablecolumns(rows, indices):
    '''Given an iterator over rows (tuples of items) of a table,
    yield-s the items indicated by the sequence of indices.'''
    for row in rows:
        yield tuplemap(row.__getitem__, indices)

def tableupdate(rowiter, newrowiter, keyfunc0, keyfunc1=None):
    '''Returns an iterator over rows of a new table, composed of
    the "new" rows produced by newrowiter and those produced by
    rowiter Designed for a limited number of rows. The keyfunc
    functions are functions of items of rowiter (arg 0) and
    newrowiter (arg 1)---they determine unique records and
    determine which records in rowiter which may be replaced by
    those of newrowiter. If keyfunc1 is unspecified, None, False,
    etc., keyfunc0 is used in its place.'''
    keyfunc1 = keyfunc1 if keyfunc1 else keyfunc0
    everynewrow = tuple(newrowiter) # store row data
    newrowkeys = set(map(keyfunc1, everynewrow)) # store row keys
    return chain(
            filter(lambda x: keyfunc0(x) not in newrowkeys, rowiter),
            everynewrow)

def tablewriterow(f, iterable, sep=' '):
    '''write-s one row to file f open for writing. Fields are
    separated by sep. Data for one row is accessed via iterable
    (could be tuple, iterator, etc.).'''
    f.write(strcat(iterable, sep) + '\n')

def tableaslines(rows, sep=SPACE):
    '''The primary argument is a table (row iterator) where ****
    ALL TABLE CELLS ARE STRINGS ****'''
    return map(compose(line, partial(str.join, sep)), rows)

def tablewrite(f, rows, sep=' '):
    '''write-s every row produced by the iterable rowiter to
    file f open for writing. Fields are separated by sep. Data
    for one row is accessed via the items produced bu rowiter
    '''
    waste(map(f.write, tableaslines(rows, sep)))
    waste(map(partial(tablewriterow, f, sep=sep), rows))

def tablekeys(rows, column):
    return set(tuple(partial(tablecolumn, n=column)(rows)))

#TODO: THIS IS GETTING TOO COMPLICATED MAYBE WANT A FUNCTION THAT
# RETURNS A MAP ALLOWS READING OVER THE SAME LINES OF A FILE OVER AND OVER
def tablekeysfromfile(file, columns=(0,), beginpos=0, nlines=None):
    return map(
    lambda c: tablekeys(compose(tablerowiter, iter,
        partial(freset, position=beginpos))(file), c), columns)

def tableduplicatekeys(rowiter, key=ident):
    '''Returns a set of keys that identify duplicate records
    represented among the items produced by rowiter.'''
    return duplicates(map(key, rowiter))

def tableduplicaterecords(rowiter, keys, key=ident):
    '''Returns a set of records that match keys by key.'''
    return set(filter(lambda x: key(x) in keys, rowiter))

def tablesort(rowiter, key):
    l = list(rowiter) # load entire table
    l.sort(key=key)
    return map(ident, l)

### BELOW: WORKING / TO BE REPLACED

def tableiterfromf(f, fnsplit=strsplit):
    '''Returns a compound iterable, where the inner iterables
    represent the words on each line of file f (arg 0).'''
    return mapchain(lineiter(f), fnsplit, iter)

def PLACEHOLDER(): # def tablereiterator
    pass
tablereiterator = partial(reiterator, None, tableiterfromf)
''' In the example below, a table containing the text
    #
            0A 0B 0C
            1A 1B
            2A 2B 2C 2D
    #
    is used to produce a compound iterator, where each inner
    iterator iterates over columns, and each outer iterator
    iterates over rows. Then, the present function is used to
    produce the iterator re, which, for example, can be used to
    view the contents of the file.
    #
            >>> fn = 'filename';   f = open(fn, 'w+')
            >>> f.write('0A 0B 0C\n1A 1B\n2A 2B 2C 2D\n')
            >>> re = tablereiterator(None, rewind(f))
            >>> # In the function call below, next produces an
            >>> # iterator over the table, each element of which
            >>> # is itself an iterator; these are map-ped to
            >>> # tuples; the map is "exploded" for print-ing.
            >>> print(*map(tuple, next(re)))
            ('0A', '0B', '0C') ('1A', '1B') ('2A', '2B', '2C', '2D')
            >>> print(*map(tuple, next(re)))
            ('0A', '0B', '0C') ('1A', '1B') ('2A', '2B', '2C', '2D')
'''

def tablecols_quick(iterator):
    '''Returns the number of columns in the table represented by
    the compound iterable (arg 0). Each inner iterable is
    assumed to produce the same number of items. In particular,
    the first inner iterable is taken as representative of
    all'''
    return len(tuple(next(next(iterator))))

def tablecols(iterator):
    '''Returns the number of columns in the table represented by
    the compound iterable (arg 0). Each inner iterable is
    assumed to produce the same number of items. In particular,
    the first inner iterable is taken as representative of
    all'''
    return max(map(count, next(iterator)))

def tablecoliter(iterator):
    '''Returns an (outer) iterator of (inner) iterators, where
    each outer iterator is an iterator over the columns of the
    table represented by the return of next([arg] iterator).
        THE COLUMNS REPEAT INDEFINITELY on a cycle beginning
    with the first column. After the last column has been
    produced, the first may again be produced with another
    next([arg] iterator) call (as in the example below).
        Example (using a file equivalent to that described in
    the tablereiterator example):
    .
            >>> re  = tablereiterator(None, rewind(f))
            >>> cre = tablecoliter(re)
            >>> print(*next(cre))
            0A 1A 2A
            >>> print(*next(cre))
            0B 1B 2B
            >>> print(*next(cre))
            0C None 2C
            >>> print(*next(cre))
            0A 1A 2A
    '''
    return map(tablecolumn, steady(iterator), cycle(tablecols(iterator)))

def tablecontentwidths(iterator):
    '''Returns an iterator over the widths of the content (i.e.,
    not including whitespace) of the columns of the table
    represente by the call next(iterator). **** ASSUMPTION ****
    Each cell of the table holds either a string or None.
    '''
    return mapchain(quota(tablecoliter(iterator), tablecols(iterator)),
            partial(filter, lambda x: x is not None), # filter out None-s
            partial(chain, ('',)), # ensure that there is at least one string of which to take it's length
            partial(map, len), # get the length of every string that gets throught the above filter
            max)

def tableformatstr(iterator): #TAGS human-readable
    '''Returns a format string for the Format Specification
    Mini-Language that can be used to produce a human-readable
    table where column widths are consistent and all cells are
    right-justified. The iterator argument is such that a the
    call next(iterator) would produce iterators over the rows of
    a table, where each cell of the table holds a string or
    None.'''
    return strcat(map(strcat, zip(
        steady('{'),
        map(str, indefinite()),
        steady(':>'),
        # Next line: No extra space needed to the left of the
        # first column; one extra space needed to the left of
        # each additional column.
        map(str, map(sum, zip(chain((0,), steady(1)), tablecontentwidths(iterator)))),
        steady('}')))) + eol()

def tablerowvalues(iterator, functions=(), fndefault=str, fill=''):
    '''Returns a map that produces, for each row of the table
    stored in file f, a tuple of values determined by evaluating
    the corresponding functions of the functions argument---a
    tuple of functions. The functions argument will be extended
    so that its length matches the number of columns in the
    table.'''
    nc = tablecols(iterator)
    return map(partial(zipapply,
            tuple(quota(chain(functions, steady(fndefault)), tablecols(iterator)))), # second argument to partial
            next(iterator)) # second argument to map

def tablefmt(f):
    '''Returns a map of formatted lines of the table stored in
    file f.'''
    re = tablereiterator(None, f)
    fil = partial(fill, fillobj='', n=tablecols(re))
    return map(
            unstar(partial(str.format, tableformatstr(re))), # map arg 0
            mapchain(tablerowvalues(re), list, fil))

def tables():
    '''Tables

    A table is stored as a text file. Each line of the file maps
    to one row of the table. The cells of each row may be
    distinguished with str.split.
        ASSUMPTIONS. Tables are assumed to have the same number
    of items in each row; expect strange behavior if the
    corresponding file does not match this assumption.
    '''
    pass

def tablejoin(*args):
    return mapchain(zip(*args), unstar(flat), tuple)

def muTable(rowwidths, value=''): ###
    '''Returns an mutable table: a tuple of lists. Each list has
    the number of items specified by the rowwidths iterable.
    Example: muTable((3,2)) returns (['', '', ''], ['', '']).'''
    return tuple(map(lambda n: [value] * n, rowwidths))

def crosstable_make(record_keys, category_keys, z=''):
    '''Returns a mutable table that can be used for cross
    tabulation. '''
    c, r = mapchain((category_keys, record_keys), frozenset, tuple)
    return tuplemap(unstar(dictzip), (
        ( c, indefinite(                              ) ),
        ( r, muTable   (quotan(steady(len(c)), len(r))) ) ))

def crosstable_setitem(ctable, record_and_category, value, cats=0, recs=1):
    r, c = record_and_category
    ctable[recs][r][ctable[cats][c]] = value
    return ctable

class crosstable:
    def __init__(self, *args, **kwargs):
        '''crosstable(record_keys, category_keys, z='') -> new
        crosstable, all values set to z'''
        if not len(args):
            self.data = tuple(crosstable(('A', 'B'), ('1', '2')))
        else:
            self.data = crosstable_make(*args, **kwargs)
    def __repr__(self):
        '''Returns a representation of the data.'''
        return repr(self.data)
    def __setitem__(self, index, value):
        '''x.__setitem__(i, y)  <==>  x[(record, category)] = y'''
        crosstable_setitem(self.data, index, value)
    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return iter(deepcopy(self.data))
    def categories(self):
        return tuple(self.data[0].keys())
    def keys(self):
        return tuple(self.data[1].keys())
    def records(self, keys=None):
        '''Returns a map over the records of the crosstable.
        Optionally, an iterable of keys may be specified; only
        those records having matching keys will be produced by
        the return.'''
        keys = filter(partial(fnin, self.keys()), keys) if keys else self.keys()
        return map(self.data[1].__getitem__, keys)
    def populate(self, compound_iterable):
        '''Populates *IN PLACE*. Iterables produced from the
        compound_iterable are assumed to contain a record id, a
        category id, and a value; in that order. The values of
        the crosstable are assigned accordingly. Reassignment of
        the same (record, category) will result in
        overwriting.'''
        for record in compound_iterable:
            self[record[:2]] = record[2]
        return self
    def export(self, keys=None, origin=''):
        '''Returns an iterator that produces the rows of the
        associated cross table. Each row is represented by a
        tuple. The first row is the header row, which contains a
        dummy value, followed by the category identifiers. Each
        successive row contains the record identifier, followed
        by the values for the categories corresponding to the
        category identifiers in the header.
            THE KEYWORD ARGUMENT origin may be used to specify
        the "top-left" value at the position that is the
        intersection of the record_key column and category key
        row .'''
        yield tuple(chain((origin,), self.categories()))
        KEYS = tuple(keys) if keys else self.keys()
        RECORDS = self.records(KEYS)
        for record in zip(map(astuple, KEYS), RECORDS):
            yield tuple(flat(*record))
    def xyz2cross(file, xyz=(0, 1, 2)):
        x, y, z = xyz
        record_keys, category_keys  = map(
            lambda c: tablekeys(compose(tablerowiter, iter, rewind)(file), c),
            (x, y))
        #printerr(record_keys, '', category_keys, sep=NEWLINE)
        xt = crosstable(record_keys, category_keys)
        xt.populate(tablecolumns(tablerowiter(iter(rewind(file))), xyz))
        return xt


