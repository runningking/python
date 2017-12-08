#!/bin/sh
./etc/profile
.~/.bash_profile
for i in 0 120 122 123 121 125;do grouplist.py -g $i ;done | grep -v "免费" 
for i in 61 62;do grouplist.py -g $i ;done | grep -v "免费"
for i in {259..600};do grouplist.py -g $i ;done | grep "免费"
for i in 16 19 38 41 45 46 48 234;do grouplist.py -g $i ;done | grep "免费" 
for i in 5 11 6 7 8 35 43 108 109 110 111 112 113 114 219 220 221;do grouplist.py -g $i ;done | grep "免费"
for i in 1 4 511;do grouplist.py -g $i ;done | grep "免费"
for i in 66 3 14 31 440 401 400 72;do grouplist.py -g $i ;done | grep "免费"
for i in 21 42 215;do grouplist.py -g $i ;done | grep "免费"
