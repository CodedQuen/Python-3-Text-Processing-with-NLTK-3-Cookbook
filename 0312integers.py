def leftout(sorted_int_iterator, sentinel=-1, default=-1):
    '''Conceptually, returns an object that contains all of the
    natural-number values left out of the sorted integer
    iterator argument.
        DETAILS. returns an iterator that iterates over the
    leftout argument, which is **** ASSUMED **** to produce
    integers (could be int-s or integer-valued float-s) in ****
    ASCENDING ORDER. **** The returned iterator yield-s the
    int-s (in ascending order, beginning with zero) that are
    absent (left out) of the argument of leftout, up to (and
    EXCLUDING the last item of the leftout argument), ****
    FOLLOWED BY A SENTINEL VALUE, **** sentinel (defaults to
    -1) and the last value from the argument of leftout (or
    default if leftout-s argument is empty). These last two
    pieces of information permit the continuation of the
    sequence by another process. For consistency, default ****
    SHOULD NOT **** be a nonnegative number.
        Originally developed as part of a process to determine
    which characters are ABSENT from a given set of characters,
    so as to find candidate separator (sep) characters.
            >>> tuple(leftout(iter((0,))))
            (-1, 0)
            >>> tuple(leftout(iter((8,))))
            (0, 1, 2, 3, 4, 5, 6, 7, -1, 8)
            >>> print(*leftout(iter(range(ord('a'), 1 + ord('z')))))
             0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
            17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
            34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
            51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67
            68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84
            85 86 87 88 89 90 91 92 93 94 95 96 -1 122
            >>> # REFORMATTED FOR CLARITY
            >>> chr(122)
            'z'
    '''
    i, k = default, 0
    for i in sorted_int_iterator:
        while k < i:
            yield k
            k += 1
        k += 1
    yield sentinel
    yield i

