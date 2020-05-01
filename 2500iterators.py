# Text Processor
# Copyright (C) 2019 D. Michael Parrish
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

def NoMore(*args, **kwargs):
    '''Intended usage: yield NoMore, item is NoMore, etc.

    HISTORY 2018-12-06 formerly accepted no arguments.'''
    assert False, 'Do not call (see help).'

def steady(value=1): #TAGS repeat constant
    '''Returns an iterator that produces value indefinitely.
    HISTORY: 2018--5-14: changed sentinel from None to NoMore;
    2018-04-11: was generator that yielded x indefinitely.'''
    return iter(constant(value), NoMore)

