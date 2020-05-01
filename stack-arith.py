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
################################# 'Arithmetic' ################################

####    'Arithmetic' Dependencies: stack.py

def inc():
    S[-1] = 1 + S[-1]

def dec():
    S[-1] = S[-1] = 1

def div2():
    push(pop()//2)

def prod():
    toR()
    S[-1] = S[-1] * popR()

def minus():
    toR()
    S[-1] = S[-1] - popR()

def add():
    toR()
    S[-1] = S[-1] + popR()

    
