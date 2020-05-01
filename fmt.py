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
def fmte(x, n=6, m=2, e='E', nmax=16):
    '''Returns a formatted float having the precision of n
    digits to the right of the decimal point and at least m
    digits in the exponent.'''
    def _expc(s): # return exponent character of e-formatted float
        return next(filter(lambda character: character in {'E', 'e'}, s))
    def _pad0(s, n): # return string padded to length n
        return ('{0:0>' + str(n) + '}').format(s)
    def _efmtes(s, n=3): # reformat e-formatted float: n e-digits
        m, e, p = s.partition(_expc(s)) # mantissa, exponent, +/-power
        return m + e + p[0] + _pad0(p[1:], n)
    def _efmt(x, n, e): # returns formatted float x: n decimals, 'e'/'E'
        return ('{0:.' + str(n) + e + '}').format(x)
    assert isinstance(x, float), 'Primary argument must be float.'
    nmax = 16 if not isinstance(nmax, int) else max(0, nmax)
    n = 6 if not isinstance(n, int) else min(max(0, n), nmax)
    m = 2 if not isinstance(m, int) else max(0, m)
    e = 'e' if e not in {'E', 'e'} else e
    return _efmtes(_efmt(x, n, e), m)

def fmtw(string_iterable, n=8):
    '''Returns a generator that yield-s the strings in
    string_iterable. The newline character is appended to every
    n-th string. An additional newline character is yield-ed
    after 
    the last string from string_iterable if that last string did not have
    a newline character appended. This function is
    similar to the UNIX/GNU function fmt, except that instead of
    individual characters being the measure of line width, it is
    words per line (arg 1). Originally intended for formatting
    tabular data or vector data. Examples:
            >>> tuple(fmtw(zipfmt(range(3)), 2))
            ('0', '1\n', '2', '\n')
            >>> tuple(fmtw(zipfmt(range(4)), 2))
            ('0', '1\n', '2', '3\n')
            >>> tuple(fmtw(zipfmt(range(5)), 2))
            ('0', '1\n', '2', '3\n', '4', '\n')
            >>> printbare(*chain('---\n', fmtw(zipfmt(range(9)), 3), '---\n'))
            ---
            012
            345
            678
            ---
            >>> printbare(*chain('---\n', fmtw(zipfmt(range(8)), 3), '---\n'))
            ---
            012
            345
            67
            ---
    '''
    column_counter = skip(cycle(n)) # columns numbered from 1; rightmost is column 0
    for string in string_iterable:
        column_number = next(column_counter)
        yield string + (NULL if column_number else NEWLINE)
    if column_number:
        yield NEWLINE

def places(nonnegative_integer): #TAGS width number format
    '''Returns the number of decimal places required to
    represent the nonnegative_integer argument in standard
    form.'''
    return len('{0:d}'.format(nonnegative_integer))

def fformat(fmt, data):
    '''STATUS: conceptual. list version of str.format'''
    lst = []

def fmtfixeddlsd(i, dig=12, v='*'):
    '''Returns string representation of the dig least significant digits of
    int i. '''
    s =('{0:0' + str(dig) + 'd}').format(i)[-dig:] 
    if not v:
        return s
    if len(s) < places(i):
        s = v * dig
    return s

def fmtlabl(iterable):
    return map(lambda i, s: strcat((str(i), ':', s)), indefinite(), iterable)

def fmtwrap(s):
    return '{' + s + '}'

def fmtstringn(fmts, n=0):
    return strcat(mapchain(enumerate(map(partial(prefix, ':'), fmts), n),
            lambda tpl: (str(first(tpl)), second(tpl)),
            strcat, fmtwrap))

# SIMPLIFIED FORMATTING (2-parameter for )

def _fmtspecsimple_pre0(string, fmtspectypeNone='.'):
    'Helper function for _fmtspecsimple_pre1'
    return map(
            lambda s: (
                    ('' if (first(s) == fmtspectypeNone) else first(s)),
                            s[1:]),
            towords(string))

def _fmtspecsimple_pre1(string, fmtspectypeNone='.'):
    'Helper function for _fmtspecsimple'
    return map(
            lambda tpl:
                    ('' if len(tpl) < 2 else \
                            '' if not tpl[1] else \
                            fmtspectypeNone + tpl[1]) + \
                    first(tpl),
            _fmtspecsimple_pre0(string, fmtspectypeNone=fmtspectypeNone))

def fmtspecsimple(string, sep=' ', fmtspectypeNone='.'):
    '''Given a string of format_specs (defined below), returns
    another string suitable for use with str.format. The
    precision should be specified for only those types
    compatible with specified precision under str.format.
        The optional argument sep specifies a string that will be
    placed between each element of the resultant format spec.
        The optional fmtspectypeNone argument specifies a
    character that will correspond to the null string as applied
    to the type parameter of the format_spec of the Format
    Specification Mini-Language. This parameter is largely
    present for consistency with the Format Specification
    Mini-Language, according to which 'd' has the same effect.

    Simplified-Format--Specification Mini-Language
    format_specs ::=
            [WHITESPACE] format_spec [WHITESPACE formatspec]+ [WHITESPACE]
    format_spec ::= type[precision]
    type ::= SAME_AS_IN_FORMAT_SPECIFICATION_MINI_LANGUAGE
    precision ::= SAME_AS_IN_FORMAT_SPECIFICATION_MINI_LANGUAGE

    Examples:
            >>> fmtspecsimple('.')
            '{0:}'
            >>> fmtspecsimple('d')
            '{0:d}'
            >>> fmtspecsimple('f2')
            '{0:.2f}'
            >>> fmtspecsimple('f2 f2 f2').format(7/22, 8/13, 10/14)
            '0.32 0.62 0.71'
    '''
    return sep.join(map(fmtwrap,
        fmtlabl(_fmtspecsimple_pre1(string))))

def fmtgridpre(iterable, maxfields=10, dimension=512):
    '''Intended as one stage of a formatter. As it stands, an
    iterable of (multidimensional) grid values is separated into
    "lines" containing no more than maxfields items per line.
    Lines are also broken at the end of each primary dimension,
    as determined by dimlength. Each line is yield-ed as a map
    that produces the corresponding grid values.'''
    assert isint(maxfields), 'fmtgridpre: maxfields must be int.'
    assert isint(maxfields), 'fmtgridpre: dimlength must be int.'
    for column in groupsmm(iterable, (maxfields, dimension)):
        for line in column:
            yield line

def zipfmt(iterable, formats=steady('{0}')):
    '''Returns a map of formatted items (strings). The number of
    items produced by the return is determined by zip-ping the
    two arguments.'''
    return map(lambda val, fmt: fmt.format(val), iterable, formats)

def hexfmt(hex_string, len_=2):
    '''Given a string representation of a hexadecimal number,
    e.g., "0xf", returns a representation of the same number,
    without the "0x" prefix. Additional zeroes are prepended if
    necessary to produce a return that is of n digits.'''
    return strpad(hex_string[2:], len_, '0')

def rep_spec_from_fortran_fmt_item(format_item): # repeat specification from Fortran format item
    return strcat(first(deal(
        (deque(), deque(format_item)),
        lambda p: p[1] and isdigit(p[1][0]))))

def rep_spec_from_fortran_data_ed_descr(data_edit_descriptor): # repeat specification from Fortran data edit descriptor
    rs = rep_spec_from_fortran_fmt_item(data_edit_descriptor)
    rs = rs if rs else '1'
    return int(rs)

