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


################################################################

def dictitem(dictionary):
    '''Returns an arbitrary item from the dictionary argument.'''
    return next(iter(dictionary.items()))

def update(obj, *args, **kwargs):
    '''Wrapper function for dict.update, set.update, etc.
    Returns the modified *IN PLACE* primary argument.'''
    obj.update(*args, **kwargs); return obj

# COMMON dict-s

# Months of the Year

def monthsasMMM():
    return ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')

def monthsasint():
    return tuple(range(1, 1 + 12))

def monthsasMM():
    from functools import partial
    return list(map(partial(fmtfixeddlsd, dig=2), monthsasint()))

def dictmonthasMMM2monthasint():
    'make dict month-as-MMM to month-as-int'
    return dict(zip(monthsasMMM(), monthsasint()))

def dictmonthasMMM2monthasMM():
    'make dict month-as-MMM to month-as-MM'
    return dict(zip(monthsasMMM(), monthsasMM()))

def dicttriv(seq):
    return dict(zip(seq, range(len(seq))))

################################################################
# dict FUNCTIONS

def rdict(dictionary):
    '''If possible, returns the inverse of the 1:1 dictionary.
    If the dictionary argument is 1:many, not all original items
    will be represented in the return (no duplicate keys). Fails
    if any values are unhashable (and therefore cannot become
    keys of the reverse dict).'''
    return dict(mapchain(dictionary.items(), reversed, tuple))

def dictis1to1(dictionary):
    return count(dictionary.keys()) == count(dictionary.values())

def dictfromkv(key, value=None):
    return {key: value}

def dictprint(dictionary, keysep=': ', file=stdout):
    '''prints the keys and values of a dict. For each key,
    print-s the key, then calls function on the associated
    value. HISTORY: changed end to keysep (spearates keys from
    values)'''
    for k in dictionary:
        print(k, end=keysep, file=file)
        print(dictionary[k], file=file)

def dictkv(dictionary, key, default=()):
    '''Returns a tuple contianing the dictionary key-value pair
    specified by key, provided that key is in dictionary.
    Otherwise returns default. Compare with
    tuple(dictionary.items()).'''
    return key, dictionary[key] if key in dictionary else default

def dictslice(dictionary, keys):
    '''Returns a new dict composed of the key-value pairs in
    dictionary, as specified by keys.'''
    return dict(filter(len, map(partial(dictkv, dictionary), keys)))

def dictnicepop(dictionary, key):
    '''Possibly modifies dictionary *IN PLACE* and returns the
    modified dictionary. Removes item with key key.'''
    if key in dictionary:
        dictionary.pop(key)
    return dictionary


# ONE-TO-MANY dict-S omdict*
#
# A ONE-TO-MANY dict IS A dict WHERE EVERY VALUE IS A list,
# tuple [, OR ?]. THESE dict VALUES ARE CONSIDERED TO BE THE
# "MANY" IN A ONE (key)-TO-MANY RELATIONSHIP.

def omdictcollapsed(dictionary):
    '''Returns a modified copy of the one-to-many dictionary.
    Each of the values in the copy is the frozenset of the
    values of the argument. Example:
            >>> dict(omdictcollapsed({'foo': (2,3,3,4,4,5)}))
            {'foo': frozenset({2, 3, 4, 5})}
    '''
    return dict(onetomany(
        (first, compose(frozenset, second)),
        iter(dictionary.items())))

def omdictitemexpand(item):
    '''Returns an iterator of key-value pairs that together
    represent the single one-to-many dict item. Example:
            >>> tuple(omdictitemexpand(next(iter({0: ['nothing', 'void']}.items()))))
            ((0, 'nothing'), (0, 'void'))
    '''
    return zip(steady(first(item)), second(item))

def omdictexpandeditems(dictionary):
    '''Returns an iterator of key-value pairs of the one-to-many
    dictionary argument. Example:
            >>> tuple(omdictexpandeditems(next(iter({0: ['nothing', 'void'], 1: ['one', 'only']}.it
            ((1, 'a'), (1, 'b'), (2, 'a'), (2, 'c'))
    '''
    return train(map(omdictitemexpand, iter(dictionary.items())))

def omdictrev(dictionary):
    '''Returns a dict where each of the many values of the
    argument are keys and each of the keys of the argument are
    values. Only one key of the argument is matched with each
    unique value of the argument. Example (note that since 'a'
    occurs under more than one key, all but one value is lost;
    which value is kept is not determined a priori):
            >>> omdictrev({1: ('a', 'b'), 2: ('a', 'c')})
            {'a': 2, 'c': 2, 'b': 1}
    *WARNING* Although one-to-many dicts can, in principle,
    store an indefinite number of items, generation of the
    reversed one-to-many dict forces evaluation, which will not
    terminate if there are an indefinite number of items to
    evaluat.
    '''
    return dict(tuple(mapchain(
        omdictexpandeditems(dictionary),
        reversed,
        tuple)))

def omdictisempty(dictionary):
    '''Returns whether the one-to-many dictionary has no values.'''
    return not bool(take(flat(*chain(set(dictionary.values())))))

def omdictnewkey(dictionary, key): # one to many
    '''Possibly modifies dictionary *IN PLACE* and returns the
    modified dictionary. If key is not already found in
    dictionary, add a key-value pair according to key, where the
    value is an empty list.'''
    if key not in dictionary:
        dictionary.update({key : []})
    return dictionary

def omdictpopitemnice(omdictionary, key, index):
    '''Returns a duple. If key is not in the one-to-many
    dictionary, the duple is empty. If the key is present, the
    first item of the duple is the key. If the multivalue
    associated with the key has a value at the index specified,
    the second item of the duple is that value.'''
    if key not in omdictionary:
        return ()
    if rangecheck(omdictionary[key], index):
        return key, omdictionary[key].pop(index)
    else:
        return key,

def omdictpopvaluenice(omdictionary, key, index, default=None):
    '''Modifies the one-to-many dicitonary *IN PLACE*. Returns
    the value pop-ed from the multi-value corresponding to key.'''
    item = omdictpopitemnice(omdictionary, key, index)
    if len(item) < 2:
        return default
    return second(item)

def validkeys(dictionary, keys):
    return filter(partial(fnin, dictionary), keys)

def dictitembykey(dictionary, key):
    '''Returns a single item from the dictionary argument, or ()
    if the key is not valid.'''
    if key not in dictionary:
        return ()
    return (key, dictionary[key])

def subdict(dictionary, keys):
    '''Returns a new dictionary having the items specified by
    keys, provided they exist.'''
    return dict(map(
        partial(dictitembykey, dictionary),
        validkeys(dictionary, keys)))

def omdictpopvalues(omdictionary, items):
    '''Modifies the one-to-many dictionary *IN PLACE*. Removes
    the values specified by the items argument (which could be a
    value returned by dict.items), the items of which are duples
    where the first item is a key of the one-to-many dictionary
    and the second is an index into the corresponding multivalue
    of the one-to-many dictionary. Any invalid items result in
    no action. Returns a tuple of the popped key-value duples.'''
    return omdict(filter(
        compose(partial(less, 1), len),
        map(
            lambda x: partial(omdictpopitemnice, omdictionary)(*x),
            items)))

def omdictappendvalue(dictionary, key, value): # one to many
    '''Appends value to the entry of dictionary identified by
    key. Raises KeyError if key does not exist, otherwise
    returns the *MODIFIED* dicitonary.'''
    dictionary[key].append(value)
    return dictionary

def omdictappend(dictionary, key, value):
    '''Appends value to the entry of dictionary identified by
    key, which is created if it does not already exist. Returns
    the *MODIFIED* dictionary.'''
    if key not in dictionary:
        omdictnewkey(dictionary, key)
    return omdictappendvalue(dictionary, key, value)

def omdictappendvalues(omdictionary, items): # one to many
    '''Returns the modified *IN PLACE* omdictionary. Provided
    that the keys of dictionary are in omdictionary, the
    corresponding values of dictionary are appended to the
    values of the omdicitonary.'''
    for item in items:
        if first(item) in omdictionary:
            omdictappendvalue(omdictionary, *item),
    return omdictionary

'''
def omdictupdate # PLACEHOLDER: use dict.update
'''

def omdict(iterable): # one to many
    '''Returns a one-to-many dictionary. The compound iterable
    argument produces iterable objects, which, in turn, produce
    exactly two items---typically, iterable produces duples.
    Returns a dict where each key is mapped to a list
    containing one, or more values, in the order
    encountered in the iterable argument. Example:
            >>> omdict( ( ('a', 1), ('b',2), ('b',3) ) )
            {'a': [1], 'b': [2, 3]}
    '''
    d = dict()
    waste(map(unstar(partial(omdictappend, d)), iterable))
    return d

def omdictis1to1(dictionary):
    '''One-to-many dictionary is one-to-one. Returns bool
    indicating whether this is the case.'''
    return all(mapchain(dictionary.values(), len, partial(argswap(less), 2)))

def omdictclean(dictionary):
    '''Returns a modified copy of dictionary, where items
    corressponding to empty-list values in dictionary are
    absent.'''
    return dict(filter(second, dictionary.items()))

def omdictnew(keys_iterable):
    '''Returns a new one-to-many dictionary whose keys are
    produced from the keys_iterable. Values of the return-ed
    dict are empty list-s.'''
    return dictzip(keys_iterable, map(deepcopy, steady([])))

def omdictempties(dictionary):
    return filter(lambda key: un(len)(dictionary[key]), dictionary.keys())

def omdictmultivaluelens(omdictionary): #TAGS len length multivalue one-to-many
    '''Returns a dict whose keys match those of the argument and
    whose values match the len of the values of argument.'''
    return dict(map(lambda key: (key, len(omdictionary[key])),
        omdictionary.keys()))

def omdictsingletons(dictionary):
    '''Returns an iterator over all of the keys which are
    associated with singleton values.'''
    return map(first, filter(
        lambda item: second(item) == 1,
        omdictmultivaluelens(omdictionary)))

def omdictmultivalues(dictionary):
    '''Returns an iterator over all of the keys which are
    associated with mulitvalues.'''
    return filter(lambda key: 1  < len(dictionary[key]), dictionary.keys())

def omdictsplit(dictionary):
    return (dictslice(dictionary, omdictempties(dictionary)),
            dictslice(dictionary, omdictsingletons(dictionary)),
            dictslice(dictionary, omdictmultivalues(dictionary)))

def omdictfirst(dictionary):
    '''Returns a dict containing keys to non-empty values of
    dictionary. Each value of the returned dict is the first
    value among the the multivalues associated with the
    corresponding key of the dictionary.'''
    return dict(map(
            lambda item: (first(item), first(second(item))),
            omdictclean(dictionary).items()))

def omdictprint(dictionary, function=partial(print, TAB), keysep=':\n', file=stdout):
    '''prints the keys and values of a dict. For each key,
    print-s the key, then calls function on the associated
    value. HISTORY: changed end to keysep (spearates keys from
    values)'''
    for k in dictionary:
        print(k, end=keysep, file=file)
        for item in dictionary[k]:
            function(item)

def findall(enumeration):
    '''c.f. findevery. The argument is an iterator of (value, key) pairs. Keys
    and values may occur multiple times.  Returns a dict where
    each key is mapped to a list containing every value
    (including any copies) associated with that key.  Compare
    and contrast with dict(mapping).'''
    return omdict(map(flipped, enumeration))

def mget(d, keys):
    '''Multiple get. Named with allusion to ftp mget.'''
    return tuple(map(d.get, keys))

def dictzip(keys, values):
    return dict(zip(keys, values))

def dictnegate(d):
    for key in d:
        d.update({key: -d[key]})
    return d

def subdict(orig, keys):
    '''Returns a copy of d with only the key-value pairs specified by keys.'''
    d = {}
    for k in keys:
        d.update({k: orig[k]})
    return d

def kv(iterable):
    return filter1(groups(iter(iterable)))

def dictfromstr(st):
    '''Returns a dict as represented by the str st. Key-value
    pairs are separated by whitespace. Within a key-value pair,
    whitespace separates the two. All keys and values in the
    returned dict are strings. Example:
    .
            >>> dictfromstr('frodo 1 sam 2')
            {'frodo': '1', 'sam': '2'}
    '''
    return dict(fullgroups(iter(st.split())))

'''
def geteach(d, keys): # use map(d.get, keys)
'''
