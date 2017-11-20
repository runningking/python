#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###使用__slots__
_
class Student(object):
	__slots__ = ('name','age') #定义特殊变量__slots__，限制class实例能添加的属性

class GraduateStudent(Student):
	pass

s = Student()
s.name = 'KING'
s.age = '98'

try:
	s.score = 96
except AttributeError as e:
	print ('ATTRIBUTEERROR:',e)

g = GraduateStudent() #__slots__定义的属性仅对当前实例起作用，对继承的子类不起作用
g.score = 99
print 'g.score=',g.score
