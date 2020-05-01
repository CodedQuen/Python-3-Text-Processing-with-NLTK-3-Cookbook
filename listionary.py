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
ly = {'*':[], '**':{'Scratch': None, 'NextKey': 0, 'Values': {}}} # positional and named data

ly.update({'view': lambda self: (self['*'], self['**'])})

print('view:', ly['view'](ly))

ly.update({'items': lambda self: () if 'Values' not in
    self['**'] else self['**']['Values'].items()})

print('items:', *ly['items'](ly))

ly.update({'nextkey': lambda self: (
    self['**'].update({
        'NextKey':
        1 + self['**']['NextKey']}),
    self['**']['NextKey'])[-1]})

print('nextkey:', ly['nextkey'](ly))

ly.update({'keys': lambda self: self['**']['Values'].keys()})

print('keys:', *ly['keys'](ly))

ly.update({'append':
    lambda self, item: (
        self['**'].update({'Scratch': self['nextkey'](self)}),
        self['**']['Values'].update({self['**']['Scratch']: item}),
        self['**']['Scratch'])[-1]})

# append returns the index of the appended item

print('appended:', ly['append'](ly, 42))
print('appended:', ly['append'](ly, 43))

print('keys:', *ly['keys'](ly))

print('items:', *ly['items'](ly))

'''
ly.update({'pop':
    lambda self:
        self['*'].pop()})


print(ly['append'](ly, 42))
print(ly['append'](ly, 43))


'''
