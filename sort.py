#!/usr/bin/env python2
# -*- coding: utf-8 -*-
L = [('Bob',75),('Adam',90),('Bart',66),('Lisa',88)]
def by_name(t):
	return t[0]

def by_score(t):
	return t[1]

l = sorted(L,key=by_score,reverse=True)
print (l)
name=by_name.__name__
print (name)
