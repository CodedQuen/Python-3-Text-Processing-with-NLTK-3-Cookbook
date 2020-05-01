def quotan(iterable, n=1):
    '''"Quota En" Returns a generator that produces the next n
    items from iterable, or all of the items, if there are n or
    fewer available. HISTORY 2018-12-01 n can be any value, but
    if it is not an int, it is set to 0 .'''
    for dummy, item in zip(
            () if not isint(n) else steady() if n < 0 else range(n),
            iterable):
        yield item

def quota(iterable, n=1, criterion=alwaysTrue, forerunner=deque()): ###
    '''yield-s the next items from iterable until 1) n (the
    count-limit) items have been yield-ed, 2) the criterion
    function returns False when evaluated with an item from the
    iterable, or 3) when the iterable is exhausted, whichever
    comes first.  The first value from iterable that does not
    meet the criterion is stored in forerunner, an appendable
    object.  DETAILS: a negative value of n implies no
    count-limit. The variable-name forerunner is intended to
    suggest that the value appended there might be considered to
    be the first of the next class of values in the iterable.
    "Forerunner": noun, "A person or thing that precedes the
    coming or development of someone or something else"---OED.
    HISTORY 2018-08-29: revised docstring; 2018-05-11: changed
    to allow for criterion; 2018-05-07: changed so that negative
    n should cause iterable to be exhausted. REFERENCE: OED
    https://en.oxforddictionaries.com/definition/us/forerunner.
    EXAMPLE (reminder: not all iterable-s are iter-ators):
    >>> # Example 1 (iterator):
    >>> it=iter(range(9))
    >>> print(*quota(it, 3))
    0 1 2
    >>> print(*quota(it, 3))
    3 4 5
    >>> # Example 2 (iterable):
    >>> rg=range(9)
    >>> print(*quota(rg, 3))
    0 1 2
    >>> print(*quota(rg, 3))
    0 1 2
    >>> # Example 3 (with criterion):
    >>> it=iter(range(9));   fore=deque()
    >>> print(*quota(it,
    ...         n=-1,
    ...         criterion=partial(argswap(less), 4),
    ...         forerunner=fore))
    0 1 2 3
    # Storing the forerunner allows us to effectively restore the
    # iterator to the condition before that item was pulled out.
    >>> print(*chain(astuple(fore.pop()), it))
    4 5 6 7 8
    '''
    #printerr('quota (entry): n:', n)
    #n = -1 if n is None else n
    #assert isinstance(n, int), 'quota: n must be int or None.'
    #if n:
    for item in quotan(iterable, n):
        if not criterion(item):
            forerunner.append(item);   break
        yield item
        #n -= 1
        #if not n:
            #break
