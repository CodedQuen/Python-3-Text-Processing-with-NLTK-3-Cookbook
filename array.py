def narraylines(fields, dimensions, breaks=True):
    '''Returns the number of lines required to store an array of
    the given dimensions, where the maximun number of values per
    line is equal to fields (arg 0).  The "fastest" dimension is
    given first.  Line breaks are / will be placed between rows
    ("fastest" dimension) according to breaks.  Each line has a
    number of values equal to fields (or has the number of
    values needed to complete a row if breaks). The last line
    has the number of values needed to complte the last row.'''
    assert isint(fields), 'fields must be int'
    assert all(map(isint, dimensions)), 'all dimensions must be int'
    assert 0 < fields, 'fields must be positive'
    if not dimensions:
        return 0
    assert all(map(partial(less, 0), dimensions)), 'all dimensions must be positive'
    dimensions = dimensions + ((1,) if len(dimensions) < 2 else ())
    p1 = unstar(product)(dimensions[1:])
    return \
        p1 * idivup(first(dimensions), fields) if breaks else \
        idivup(p1 * first(dimensions), fields)


