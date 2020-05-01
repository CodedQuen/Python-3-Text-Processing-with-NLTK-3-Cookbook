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

# TIME CONVERSION. SI UNIT OF TIME IS seconds. 'from x' implies
# 'to seconds.' similarly for the 'to' functions

def fromminutes(x): # tags: time
    return 60 * x

def fromhours(x): # tags: time
    return fromminutes(60 * x)

def fromdays(x): # tags: time
    return fromhours(24 * x)

def tominutes(x): # tags: time
    return preferint((lambda x: x / 60, lambda x: x // 60))(x)

def tohours(x):
    return tominutes(x) / 60

def todays(x):
    '"to days"'
    return tohours(x) / 24

def datesdoc():
    '''Herein, the standard time datum is Julian Day UT1. names
    containing e.g., "fromgreg" imply "tojulianday" suffixes:
    greg: refers to Gregorian Calendar'''
    pass

def isdate(x):
    '''Intended for use in assert-ions or similar. To the
    author's knowledge, all conventional dating schemes can be
    represented as an integer (e.g., Julian Day) or a sequence
    of nonnegative integers (e.g., Gregorian Calendar date).'''
    return istupleofpositiveints(x)

def splitisodates(st):
    '2017-11-08T16:52:42+00:00'
    return list(map(lambda x: int(x), ''.join(list(map(lambda x: x if x.isdigit() else ' ', list(st)))).split(' ')))

def gregdoc():
    '''
    Gregorian Calendar begins on 1522-10-15
    1582-12-31T12:00 UT1 = 2299238 JD
    The fictitious
    1581-12-31T12:00 UT1 = 2298873 JD (365 days before 1582-12-31)
    '''
    pass

def tomsofficedatenumber(jd):
    '''Returns a float representing the date as stored
    numerically by MS Excel. Excel falsely assumes that
    Gregorian Year 1900 was a leap year. This function account
    for this assumpiton. Reference: https://support.microsoft.
    com/en-us/help/214326/excel-incorrectly-assumes-that-the-
    year-1900-is-a-leap-year'''
    return jd - 2415019.5 + (1, 0)[jd < 2415079.5] # i.e., use a shift of 2415018.5 if jd is not before March 31, 1900

def fromyeargreg1581():
    '''Returns the JD (int) corresponding to the fictitious
    Gregorian 1581-12-31T12:00 UT1'''
    return 2298873

def isyearleapgreg(Gregorian_year):
    year_is_divisible_by = partial(divisible, Gregorian_year)
    return (
        year_is_divisible_by(400) or
        year_is_divisible_by(  4) and not year_is_divisible_by(100))

def daysinyeargreg(y):
    'Returns number of days in Gregorian Year y.'
    return 365 + isyearleapgreg(y)

def iteryearsgreg():
    'Returns an iterator of Gregorian Years, beginning with 1582.'
    return map(partial(int.__add__, 1582), indefinite())

def iteryearlengthgreg():
    '''Returns an iterator of the number of days in each
    Gregorian Year, beginning with the year 1582.'''
    return map(daysinyeargreg, iteryearsgreg())

def iterfromyeargreg(): # tags: gregorian end of year eoy jd julian day
    '''Returns an iterator of the Julian Day Number (int) asso-
    ciated with the last day of each Gregorian Year (i.e.
    December 31) beginning with the fictitious year 1581.
    Having the JD for the fictitious 1581 facilitates 1582 calc-
    ulations. Note that the JD returned for 1581 is different
    from that associated with Dec. 31, 1581 in the Navy's Julian
    Day Converter (see references), because therein, there is a
    switch to the Julian Calendar prior to Gregorian October 15,
    1582.'''
    yl = iteryearlengthgreg()
    jd = fromyeargreg1581()
    while True:
        yield jd
        jd += next(yl)

def dayseachmonthgreg(isleapyear): # old name: dayseachmonthgreg dayseachmonthgreg
    '''Given a bool indicating whether the leap year calendar is
    under consideration, returns a tuple whose values specify
    the number of days in the corresponding month, e.g.,
    dayseachmonthgreg[True][2] returns 29, as there are 29 days
    in February (month 2) during a leap year.'''
    Jan, Mar_Dec = (31,), (31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return (Jan + (28,) + Mar_Dec,   Jan + (29,) + Mar_Dec)[isleapyear]

def cumulativedayspermonthgreg(isleapyear):
    return accumulate(dayseachmonthgreg(isleapyear))

def greglastdomgreg(ymd): # old name: greglastdomgreg
    '''Returns the last day of the month given the ymd argument,
    assuming the Gregorian Calendar.'''
    y, m, d = ymd
    return dayseachmonthgreg(isyearleapgreg(y))[m]

def gregpredgreg(ymd): # old name: gregorianpreviousday:
    '''Given a day on the Gregorian Calendar, ymd, returns the
    PREDecessor (previous day), ymd. E.g.,
    gregpredgreg((2000, 3, 1)) returns (2000, 2, 29)'''
    y, m, d = ymd
    if (m == 1) and (d == 1): # Jan 1 exception
        return y - 1, 12, 31
    if (m == 3) and (d == 1): # only case where leap year maters
        return y, 2, dayseachmonthgreg(isyearleapgreg(y))[2]
    if (d == 1): # First day of month exception
        m -= 1
        return y, m, dayseachmonthgreg(0)[m]
    return y, m, d - 1 # typical case

def ishms(hms):
    if not isinstance(hms, tuple):
        return False
    if not (len(hms) == 3):
        return False
    h, m, s = hms
    if not isint(h):
        return False
    if not isint(m):
        return False
    if not isscalar(s):
        return False
    if (h < 0) or (23 < h):
        return False
    if (m < 0) or (59 < m):
        return False
    if (s < 0) or (60 <= s):
        return False
    return True

def isygreg(y):
    '''Returns a bool indicating whether the year specified
    (int) is a valid year on the Gregorian Calendar.'''
    return isint(y) and 1581 < y

def ismgreg(m):
    '''Returns a bool indicating whether the month specified
    (int) is a valid month on the Gregorian Calendar. Does not
    consdier the year.'''
    return isint(m) and (0 < m) and (m < 13)

def isymgreg(ym):
    if not isinstance(ym, tuple) and (len(ym) == 2):
        return False
    if not (len(ym) == 2):
        return False
    y, m = ym
    if not (isygreg(y) and ismgreg(m)):
        return False
    if (y == 1582) and (m < 10):
        return False

def isymdgreg(ymd):
    '''Returns a bool indicating whether the ymd argument
    represents a valid date on the Gregorian Calendar.
    isymdgreg(1852, 10, 14) should return False, as that is the
    fictitious day before the first day of the Calendar.'''
    assert isdate(ymd)
    ymd = tuplefy(ymd)
    if not len(ymd) == 3:
        return False
    # ymd is a tuple of int-s
    y, m, d = range(3)
    if (ymd[m] < 1) or (12 < ymd[m]):
        return False # bad month
    if ymd[y] < 1582:
        return False # Gregorian Calendar starts in 1582
    if (ymd[y] == 1582) and (ymd[m] < 10):
        return False # Gregorian Calendar starts in October 1582
    if (ymd[y] == 1582) and (ymd[m] == 10) and (ymd[d] < 15):
        return False # Gregorian Calendar starts Octber 15, 1582
    if ymd[d] < 1:
        return False
    if ymd[d] > greglastdomgreg(ymd):
        return False
    return True

def dayofyeargregorian(ymd):
    '''Given (YYYY, MM, DD), returns the day of the year, where
    Jan 1 is day 1, Feb 1 is day 32, and so on.'''
    yy, mm, dd = range(3) # indices for Leap Days, Month, Day
    ld = isyearleapgreg(ymd[yy]) # leap days
    dm = sum(map(lambda m: dayseachmonthgreg(ld)[m], range(1, ymd[mm]))) # days passed in the previous month
    return dm + ymd[dd]

def fromyeargregorian(y=None): # old name: gregorianyeartojuliandays tags: JD julian days
    '''Returns the Julian Day Number for Noon (UT1), Dec 31
    (i.e., last day of the year) in the Gregorian Year specified
    by the argument.  WARNING: In development: does not extend
    back to the first Gregorian year; call this funciton with no
    argument to have this function return an int equal to the
    first Gregorian year for which this funciton can produce the
    Julian Day Number.'''
    if y is None:
        return 1600
    assert isint(y)
    minyear = fromyeargregorian()
    assert not(y < minyear), 'fromyeargregorian: not designed for years < ' + str(minyear) + '.'
    jd1600 = 2305813 # EOY 1600; source: "Julian Date Converter," http://aa.usno.navy.mil/data/docs/JulianDate.php
    yy = y - 1600 # full years passed since EOY 1600
    E  = yy // 400 # full Epochs passed since EOY 1600
    C  = yy // 100 -   4 * E # full centuries passed since end of previous epoch
    O  = yy //   4 - 100 * E -  25 * C # full "olympiads" passed since end of previous century
    Y  = yy        - 400 * E - 100 * C - 4 * O # full years passed since end of previous olympiad since end of previous century since end of previous epoch
    dE = E * (303 * 365 + 97 * 366) # Number of days in the Epochs passed
    dC = C * ( 76 * 365 + 24 * 366) # number of days in the full centuries passes since the end of the previous epoch
    dO = O * (  3 * 365 +  1 * 366) # number of days in the full "olimpiads" passed since end of previous century since end of previous epoch
    dY = Y * 365 # number of days in the full years passed since the end of the previous olympiad since the end of the previous century since the end of the previous epoch
    return jd1600 + sum((dE, dC, dO, dY))
    #return E, C, Y, dE, dC, dO, dY

def fromdategreg(ymd): # old name: fromdategregorian
    '''Returns the Julain Day Number for Noon (UT1) (int) on the
    Gregorian Date indicated by the argumnet.'''
    return fromyeargregorian(ymd[0] - 1) + dayofyeargregorian(ymd)

def topriormidnightdatum(jds):
    '''Given the Julian Day (int or float), IN UNITS OF SECONDS,
    returns a time-value adjusted as if the scheme were to begin
    days 12 hours EARLIER (e.g. at the midnight prior to the
    noon at which the JD begins).  Example: for
    2000-01-01T00:00 UT1 = 2 451 544.5 JD, this function returns
    2 451 544.
    Subtracting the input from the output of this function
    should yield the time on the UT1 clock, IN SECONDS.
    '''
    return jds + fromhours(12)

def totimezone(jdh, units=24, offset=-5):
    '''Given the Julian Day in units consistent with the
    parameter of the same name, returns the corresponding '''
    assert 1 < 0, 'This battlestation is not yet operational.  (function in preparation.)'
    return jdh

def toydoygreg(jd, iguess=1581, jdmemo=None, maxjd=2816787): # old name: toyeargreg
    '''Given a Julian Day Number (int), returns the associated
    Gregorian Year. Note: An integral Julian Day Number
    corresponds to a time of day of noon.  TEST WITH, E.G.:
    >>> with open('t:/test-jd.txt', 'w') as f:
    ...     for jd in range(2299161, 2299161+366*(2020-1581)):
    ...             yr = toyeargreg(jd, iguess=1581, jdmemo=jdm)
    ...             print(jd - jdm(yr-1), yr, jd, file=f)
    
    '''
    printerr('(STATUS)', 'toydoygreg (A)')
    if not isint(jd):
        return NaN()
    printerr('(STATUS)', 'toydoygreg (B)')
    if not jdmemo:
        jdmemo = setargdatum(memo(iterfromyeargreg()), 1581)
        printerr('(STATUS)', 'toydoygreg (B.1)')
        printerr('(STATUS)', 'type(jdmemo):', jdmemo)
        printerr('(STATUS)', 'jememo(1581)', jdmemo(1581))
    printerr('(STATUS)', 'toydoygreg (C)')
    #for i in rangeincl(1581, 2014):
        #printerr(jdmemo(i))
    #printerr('(STATUS)', 'toydoygreg (D)')
    #input()
    #print('toyeargreg: jd:', jd)
    #print('toyeargreg: jdmemo(1581):', jdmemo(1581))
    printerr('(STATUS)', 'toydoygreg (H)')
    assert jdmemo(1581) <= jd, 'not valid prior to fictitious Gregorian Year 1581.'
    printerr('(STATUS)', 'toydoygreg (I)')
    assert jd <= maxjd, 'Julian Day Number parameter exceeds maxjd parameter:' + str(jd) + '>=' + str(maxjd)
    printerr('(STATUS)', 'toydoygreg (J)')
    assert jdmemo(iguess) <= jd, 'Bad initial guess.'
    '''
                YEAR                 YEAR               YEAR
                I - 1                 I                 I + 1
        |                   |                   |                   |
        |                   | v      v        v |                   |
    ... |[ ][ ][ ... ][ ][X]|[ ][ ][ ... ][ ][X]|[O][ ][ ... ][ ][X]| ...
        |                   |                   |                   |
        |                   |                   |                   |
        X: JD corresponding with Dec. 31 of YEAR J
        v: possible value for jd (2 edge cases and a typical case)
        O: first day beyond YEAR I = 1
        Find I for a given value of jd
    '''
    y = iguess
    printerr('(STATUS)', 'toydoygreg (M)')
    for yr in map(partial(int.__add__, iguess), indefinite()): # the years we'll guess
        #print('toyeargreg: year:', yr)
        jdy = jdmemo(yr)
        j = 1 + jdy # j is the JD of the first day of the year following year yr
        if jd < j:
            '''Provided that we start with a sufficiently small
            guess, the first time the program counter gets here,
            the year prior to that corresponding to j is the
            year corresponding to jd.'''
            break
    #print( 'toyeargreg:---\n',
            #jdy, 'is Dec 31,', yr, '\b.\n',
            #jd, 'is in Gregorian Year', yr, '\b.\n',
            #jd, 'is day', jd - jdmemo(yr-1), 'of the year.')
    return yr, jd - jdm(yr-1)

def ydoygregtomgreg(y, doy):
    '''Given the year and day of year (Gregorian), returns the
    month (Gregorian).'''
    days = cumulativedayspermonthgreg(isyearleapgreg(y))
    d = throughtovalue(deque([0]), iter(days), doy) # TO DO: CREATE MORE EFFICIENT look FUNCITON
    return days.index(*d)

def ydoygregtoymdgreg(y, doy):
    '''Given the year and day of year (Gregorian), returns the
    year, month, and day (Gregorian) as a tuple.'''
    m = ydoygregtomgreg(y, doy)
    days = cumulativedayspermonthgreg(isyearleapgreg(y))
    return y, m, doy - days[m-1]

def toymdgreg(jd):
    return ydoygregtoymdgreg(toydoygreg(jd))

def toyeargregorian(jd, guess=1600): # tags: JD julian
    '''STATUS: IN PROGRESS, PASSED CURSORY TESTING. POSSIBLY
    DEPRECATED. LATELY USING THE SIMPLER APPROACH OF toyeargreg. Given the
    Julian Day, jd (nonnegative int-eger), returns the most
    recent Gregorian Year that is not beyond Julian Day
    jd.'''
    # band year by stepping forward. FUTURE: step backward if
    # guess is too high.
    step = 1
    badguess = True
    while badguess:
        guess = max(guess, fromyeargregorian())
        g = deque([guess, guess + step]) # deque of guesses
        j = deque(map(fromyeargregorian, g)) # deque of corresponding Julian Days
        if first(j) <= jd:
            badguess = False
        else:
            guess=fromyeargregorian() # i.e., guess the minimum acceptable year
    while second(j) < jd:
        #print(g, j, jd, jd-first(j), jd-second(j))
        step *= 2 # take a bigger step
        shiftin(g, astuple(step + second(g)))
        shiftin(j, astuple(fromyeargregorian(second(g))))
    assert first(j) <= jd and jd <= second(j), 'jd not found between guess results.'
    # now do bisection until guesses are no more than one year apart.
    def f(tgj): # should not be called unless there are new guessed to make
        #print('\ntodategregorian: f: tgj:', *tgj, sep='\n', end='\n\n')
        t, g, j = tgj # target, old guesses, old JD's
        gnew = sum(g) // 2
        #print('\ntodategregorian: f: gnew:', gnew, sep='\n', end='\n\n')
        jnew = fromyeargregorian(gnew)
        which = t < jnew # False(0): jnew is not too great; True(1): jnew is too great
        gg = deque(iter(g)) # make new deques---mutability causing problems
        jj = deque(iter(j)) # make new deques
        gg[which] = gnew # replace the values that are either ...
        jj[which] = jnew # ...  even bigger or even smaller
        #print('\ntodategregorian: about to return:', t, g, j, sep='\n', end='\n\n')
        return t, gg, jj
    x, x, n = fixedpoint(f, (jd, g, j) ) # we used default comparison of equal
    return x[1][0]

def dstdates(y):
    '''Returns a duple of Gregorian dates (ymd) denoting the
    start and end of Daylight Savings Time acording to US
    Law. Reference: http://aa.usno.navy.mil/faq/docs/daylight_time.php'''
    dst={   1999: ((4, 4), (10,31)),
            2000: ((4, 2), (10,29)),
            2001: ((4, 1), (10,28)),
            2002: ((4, 7), (10,27)),
            2003: ((4, 6), (10,26)),
            2004: ((4, 4), (10,31)),
            2005: ((4, 3), (10,30)),
            2006: ((4, 2), (10,29)),
            2007: ((3,11), (11, 4)), # rule changes in 2007
            2008: ((3, 9), (11, 2)),
            2009: ((3, 8), (11, 1)),
            2010: ((3,14), (11, 7)),
            2011: ((3,13), (11, 6)),
            2012: ((3,11), (11, 4)),
            2013: ((3,10), (11, 3)),
            2014: ((3, 9), (11, 2))}
    assert y in dst, 'The dstdates function does not yet handle the year requested.'
    print('dstdates: y, dst[y]:', y, dst[y])
    return tuple(map(lambda tpl: tuple(chain( (y,), tpl )), dst[y]  )  )

def timeustostd(ymd, h, nim=0, s=0, warn=None):
    '''Given a date and time on a clock, where the clock is
    adjusted to DST during the prescribed time of year, returns
    standard time. DST rules are per US Law. Gregorian Calendar
    dates are assumed. Attempts to convert times between 01:00
    and 02:00 on "fall back" day present an ambiguous condition;
    set warn to the file parameter that should be used for a
    corresponding call to the print function that will issue a
    warning.'''
    assert isymdgreg(ymd), 'timeustostd: Date must be a date on the Gregorian Calendar.'
    assert ishms((h, nim, s)), 'timeustostd: Problem with time format.'
    # ymd is a valid Gregorian Date, and (h, nim, s) is a valid 
    dststart, dstend = dstdates(ymd[0]) # could throw error, if y out of range
    print('A', ymd, dststart, dstend)
    if ymd < dststart: # before "spring forward" day
        return ymd, (h, nim, s)
    print('B')
    if ymd == dststart: # on "spring forward" day
        if h  < 2: # before 03:00
            return ymd, (h, nim, s) # switch to DST has not yet occurred
        if h == 2:
            if warn:
                print('dsttostdusa: time with hour == 2 is invalid for "spring forward" day. Assuming clock has not yet been turned forward.', file=warn)
            return ymd, (h, nim, s)
        return ymd, (h - 1, nim, s) # h > 2, DST in effect
    print('C')
    if ymd < dstend: # during DST, before "fall back" day
        if not h: # before 01:00
            return gregpredgreg(ymd), (23, nim, s)
        return ymd, (h - 1, nim, s)
    print('D')
    if ymd == dstend: # on "fall back" day
        if not h: # hour = 0, i.e., before 01:00
            return gregpredgreg(ymd), (23, nim, s)
        if h < 2:
            if warn:
                print('dsttostdusa: ambiguous condition: clock reads between 01:00 and 02:00 on "fall back" day. Assuming clock has not yet been turned back.', file=warn)
            return ymd, (h - 1, nim, s) # before 02:00, DST still in effect
    print('E')
    return ymd, (h, nim, s) # after "fall back" day

def fromdatestr(string):
    '''str.split-s the string argument by anything that is not a
    decimal digit. Returns the result of the split. Whether the
    return represents a date depends on the interpretation of
    the argument and the result.'''
    return tuplemap(int, words(maskchars(string, keep=partial(fnin, DECIMAL_DIGITS))))

def frommdy(mdy):
    '''Receives an iterable (date) in MDY format. Returns the
    corresponding YMD format.'''
    return reordered(mdy, {2:0, 0:1, 1:2})

def tomdy(mdy):
    '''Receives an iterable (date) in ISO format (Y, M, D). Returns the
    corresponding MDY format.'''
    return reordered(mdy, {0:2, 1:0, 2:1})

def mdysort(mdy_iterable):
        return tuple(map(tomdy, sorted(list(map(frommdy, mdy_iterable)))))


'''     Reference: Julian Date Converter

        http://aa.usno.navy.mil/data/docs/JulianDate.php

        Julian dates (abbreviated JD) are simply a continuous
        count of days and fractions since noon Universal Time on
        January 1, 4713 BC (on the Julian calendar). Almost 2.5
        million days have transpired since this date. Julian
        dates are widely used as time variables within
        astronomical software.  Typically, a 64-bit floating
        point (double precision) variable can represent an epoch
        expressed as a Julian date to about 1 millisecond
        precision. Note that the time scale that is the basis
        for Julian dates is Universal Time, and that 0h UT
        corresponds to a Julian date fraction of 0.5.
        
        It is assumed that 7-day weeks have formed an
        uninterrupted sequence since ancient times. Thus, the
        day of the week can be obtained from the remainder of
        the division of the Julian date by 7.
        
        Calendar dates---year, month, and day---are more
        problematic. Various calendar systems have been in use
        at different times and places around the world. This
        application deals with only two: the Gregorian calendar,
        now used universally for civil purposes, and the Julian
        calendar, its predecessor in the western world. As used
        here, the two calendars have identical month names and
        number of days in each month, and differ only in the
        rule for leap years. The Julian calendar has a leap year
        every fourth year, while the Gregorian calendar has a
        leap year every fourth year except century years not
        exactly divisible by 400.
        
        This application assumes that the changeover from the
        Julian calendar to the Gregorian calendar occurred in
        October of 1582, according to the scheme instituted by
        Pope Gregory XIII. Specifically, for dates on or before
        4 October 1582, the Julian calendar is used; for dates
        on or after 15 October 1582, the Gregorian calendar is
        used. Thus, there is a ten-day gap in calendar dates,
        but no discontinuity in Julian dates or days of the
        week: 4 October 1582 (Julian) is a Thursday, which
        begins at JD 2299159.5; and 15 October 1582 (Gregorian)
        is a Friday, which begins at JD 2299160.5. The omission
        of ten days of calendar dates was necessitated by the
        astronomical error built up by the Julian calendar over
        its many centuries of use, due to its too-frequent leap
        years.
        
        The changeover to the Gregorian calendar system occurred
        as described above only in Roman Catholic countries.
        However, adoption of the Gregorian calendar in the rest
        of the world progressed slowly. For example, for England
        and its colonies, the change did not occur until
        September 1752. (The Unix cal command for systems
        manufactured in the U.S. reflects the 1752 changeover.)
        
        For a list of when certain countries switched to the
        Gregorian calendar, see Claus T[o]ndering's Calendar
        FAQ. More information on calendars and their histories
        can be found in E. G. Richards' "Calendars" chapter of
        the Explanatory Supplement to The Astronomical Almanac
        (ed. S. E. Urban & P. K.  Seidelmann, University Science
        Books, 2012); the "Calendars" chapter by L. E.  Doggett,
        which appeared in the 1992 edition, can also be helpful. 
        
        The modified Julian date (MJD) is related to the Julian
        date (JD) by the formula: MJD = JD - 2400000.5'''

#### BELOW: WORK IN PROGRESS

class _fromyeargreg:
    '''STATUS: NOT FUNCTIONING AS INTENDED. WORKAROUND:
    >>> fromyeargreg = setargdatum(memo(iterfromyeargreg()), 1581)
    >>> # nothing prevents you from making multiple, redundant memo's
    >>> fromyeargreg(1581) # example call
    >>> 

    Intended to produce a singleton object with a single
    member function, fromyeargreg.
            The fromyeargreg member function returns the Julian
    Day Number (int) of the last day (i.e., December 31) of the
    Gregorian year specified by the actual argument of
    fromyeargreg.
            The Julain Day Number returned is the UT1 time at
    noon on the last day of the year.
            Valid Gregorian years, beginning with 1582 (The
    Gregorian Calendar begins on October 15, 1582) are
    supported, as is the the fictitious Gregorian year 1581. The
    fictitious 1581 is supported as an aid to computing dates
    within 1582.
            The maxyear optional parameter specifies the last
    year for which the fromyeargreg member function will return
    a value; it is used to prevent accidentally creating
    a large storage requirement, should a large value be
    specified for the year (one int is stored for every year
    beyond 1580 that is used to call the function).
            Suggested usage:
    >>> jd = fromyeargreg()
    >>> jd.fromyeargreg(1582)
    >>> jd.fromyeargreg(2000)
    FUTURE: allow reassignment of maxyear
    parameter, while saving memoized data. Storage requirement:
    O(n).
    '''
    class only:
        def makethejdoffset(self, maxyear=2140):
            mem = memo(iterfromyeargreg())
            def inner(y):
                if not isint(y):
                    return
                if y < 1581:
                    return
                if y > maxyear:
                    return
                return mem(y - 1581)
            return inner
        def __init__(self, maxyear=2140):
            self.fromyeargreg = self.makethejdoffset(maxyear=maxyear)
    instance = None
    def __init__(self, maxyear=2140):
        if not fromyeargreg.instance:
            fromyeargreg.instance = fromyeargreg.only(maxyear=maxyear)
    def __getattr__(self, name):
        return getattr(self.instance, name)

def ymdcmp(ymd0, ymd1): # tags: compare dates
    '''Compare dates. Returns values consistent with the Python
    built-in funciton cmp.'''
    assert False, 'Use <, ==, > with tuples instead.'
