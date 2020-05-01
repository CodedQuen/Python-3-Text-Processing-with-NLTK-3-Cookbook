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
### 'CONSTANTS'

### Goal: do not add content that refers to the content of other files or packages
KWARG_MISSING = object() # intended use: default value for function argument---indicates that no value was specified for the corresponding argument
END_OF_ITERATOR = object() # intended use: as the 'default' argument of next. C.f. EOF, EOL
kwarg_missing = KWARG_MISSING #DEPRECATED use KWARG_MISSING
end_of_iterator = END_OF_ITERATOR #DEPRECATED use END_OF_ITERATOR
