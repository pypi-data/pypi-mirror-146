# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 20:47:35 2022

@author: chenyc
"""

# 运算符重载装饰器，春秋迭代，yondersky@126.com，2022-02-25
# 更新日期：2022-02-26

import functools
from pandas import Series, DataFrame

# 1. 基础数据

UnaryOperators = ['__pos__','__neg__']
UnaryBoolOperators = ['__invert__']
BinaryOperators = [
    '__add__', '__radd__', '__iadd__',
    '__sub__', '__rsub__', '__isub__',
    '__mul__', '__rmul__', '__imul__',
    '__truediv__', '__rtruediv__', '__itruediv__',
    '__floordiv__', '__rfloordiv__', '__ifloordiv__',
    '__mod__', '__rmod__', '__imod__',
    '__pow__', '__rpow__', '__ipow__',
]
BinaryBoolOperators = [
    '__and__', '__rand__', '__iand__',
    '__or__', '__ror__', '__ior__',
    '__xor__', '__rxor__', '__ixor__',
    '__eq__', '__ne__',
    '__gt__', '__lt__',
    '__ge__', '__le__',
]

# 2022-02-25
def UnaryFunc(operator, attr = '_ValidData', dtype = None):
    '''数据序列一元运算符'''
    
    # 2022-02-25
    @functools.wraps(operator)
    def operfunc(self):
        datafunc = getattr(getattr(self,attr),operator)
        return self.new_data(datafunc(),dtype)
    
    return operfunc

# 2022-02-25
def BinaryFunc(operator, attr = '_ValidData', dtype = None):
    '''数据序列二元运算符'''
    
    # 2022-02-25
    @functools.wraps(operator)
    def operfunc(self, other):
        try:
            datafunc = getattr(getattr(self,attr),operator)
            if isinstance(other,type(self)):
                return self.new_data(datafunc(getattr(other,attr)),dtype)
            elif isinstance(other,Series) or isinstance(other,DataFrame):
                return self.new_data(datafunc(other.values),dtype)
            else:
                return self.new_data(datafunc(other),dtype)
        except TypeError:
            return NotImplemented
    
    return operfunc

# 2. 运算符转移装饰器

# 【注】运算符转移装饰器将ArraySeries或ArrayFrame的运算符操作转移至_ValidData成员。

# 2022-02-25
def OperatorTransfer(cls, attr = '_ValidData'):
    for op in UnaryOperators:
        setattr(cls,op,UnaryFunc(op,attr))
    for op in UnaryBoolOperators:
        setattr(cls,op,UnaryFunc(op,attr,bool))
    for op in BinaryOperators:
        setattr(cls,op,BinaryFunc(op,attr))
    for op in BinaryBoolOperators:
        setattr(cls,op,BinaryFunc(op,attr,bool))
    return cls
