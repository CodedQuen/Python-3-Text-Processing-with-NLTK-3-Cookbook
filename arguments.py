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
# ARGUMENT PARSING, ETC.

def strstr_to_fnd_arg_kwa(string): #TAGS filename dicitonary arguments keyword arguments
    '''Returns a tuple containing the filename dictionary,
    string args, and string kwargs corresponding to the compound
    string argument. Example:
            >>> strstr_to_fnd_arg_kwa('* r infile w outfile* 1 2 3* k1 v1 k2 v2')
            ({'r': ['infile'], 'w': ['outfile']}, ('1', '2', '3'),
            {'k2': 'v2', 'k1': 'v1'}) 
        '''
    printerr(strcats(words('''
        strstr_to_fnd_arg_kwa (compound string to filenamd
        dictionary, arguments, and keyword arguments): expecting
        a string similar to "* r read-mode-file w
        write-mode-file* arg0 arg1* kwa0 kwa1".  Receivced...''')),
        string, sep=NEWLINE)
    sfnd, sa, skwa = strsplit0(string)
    printerr(sfnd)
    printerr(sa)
    printerr(skwa)
    printerr(strsplit0(sfnd))
    printerr(*kv(strsplit0(sfnd)))
    return omdictoffilenames(*zip(*kv(strsplit0(sfnd)))), \
            strsplit0(sa), dictfromstr(skwa)

