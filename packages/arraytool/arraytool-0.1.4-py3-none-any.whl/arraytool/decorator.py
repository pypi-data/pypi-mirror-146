# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 20:47:35 2022

@author: chenyc
"""

# arraytool包专用装饰器，春秋迭代，yondersky@126.com，2022-02-25
# 更新日期：2022-04-16

# 【注】通用装饰器位于pytool.py文件中。

import bisect
import numpy as np
from pandas import Series, DataFrame

from arraytool.pytool import tsapply, IsSingleType

# 1. 运算符转移装饰器

# 1.1 基础数据

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

# 1.2 运算符函数装饰器

# 2022-02-25
def UnaryFunc(operator, attr = '_ValidData', dtype = None):
    '''数据序列一元运算符'''
    
    # 2022-02-25
    def operfunc(self):
        datafunc = getattr(getattr(self,attr),operator)
        return self.new_data(datafunc(),dtype)
    
    return operfunc

# 2022-02-25
def BinaryFunc(operator, attr = '_ValidData', dtype = None):
    '''数据序列二元运算符'''
    
    # 2022-02-25
    def operfunc(self, other):
        try:
            datafunc = getattr(getattr(self,attr),operator)
            if isinstance(other,self.__class__):
                return self.new_data(datafunc(getattr(other,attr)),dtype)
            elif isinstance(other,Series) or isinstance(other,DataFrame):
                return self.new_data(datafunc(other.values),dtype)
            else:
                return self.new_data(datafunc(other),dtype)
        except TypeError:
            return NotImplemented
    
    return operfunc

# 1.3 运算符转移装饰器

# 2022-02-25
def OperatorTransfer(cls, attr = '_ValidData'):
    '''
    运算符转移装饰器。
    【注】运算符转移装饰器将ArraySeries或ArrayFrame的运算符操作转移至_ValidData成员。
    '''
    for op in UnaryOperators:
        setattr(cls,op,UnaryFunc(op,attr))
    for op in UnaryBoolOperators:
        setattr(cls,op,UnaryFunc(op,attr,bool))
    for op in BinaryOperators:
        setattr(cls,op,BinaryFunc(op,attr))
    for op in BinaryBoolOperators:
        setattr(cls,op,BinaryFunc(op,attr,bool))
    return cls

# 2. 统计函数装饰器

# 2.1 基础数据

StatOperators = ['abs','sign']
NAStatOperators = [
    'mean', 'median', 'sum', 'prod',
    'max', 'min', 'argmax', 'argmin',
]
CumNAStatOperators = ['cumsum','cumprod']

# 2.2 统计函数装饰器

# 2.2.1 通用函数装饰器

# 2022-04-15
def StatFunc(operator, attr = '_ValidData'):
    '''数据系列统计函数'''
    
    # 2022-04-15
    def operfunc(self, **kwargs):
        '''统计函数，参见numpy同名函数'''
        return self.new_data(getattr(np,operator)(getattr(self,attr),**kwargs))
    
    return operfunc

# 2.2.2 数据系列

# 2022-04-03
def CumNAStatFuncSeries(operator, attr = '_ValidData'):
    '''数据系列累计统计函数（含NA相关参数）'''
    
    # 2022-04-03
    def operfunc(self, skipna = True, **kwargs):
        '''累计统计函数，参见numpy同名参数'''
        data = getattr(self,attr)
        if skipna:
            if data.dtype==object:
                data = data.astype(float)
            rt = getattr(np,'nan'+operator)(data,**kwargs)
        else:
            rt = getattr(np,operator)(data,**kwargs)
        return self.new_data(rt)
    
    return operfunc

# 2022-03-09
def NAStatFuncSeries(operator, attr = '_ValidData'):
    '''数据系列统计函数（含NA相关参数）'''
    
    # 2022-03-09
    def operfunc(self, skipna = True, **kwargs):
        '''统计函数，参见numpy同名函数'''
        data = getattr(self,attr)
        if skipna:
            if data.dtype==object:
                data = data.astype(float)
            return getattr(np,'nan'+operator)(data,**kwargs)
        else:
            return getattr(np,operator)(data,**kwargs)
    
    return operfunc

# 2.2.3 数据系列分组

# 2022-03-19
def NAStatFuncSeriesGroupBy(operator):
    '''数据系列分组统计函数（含NA相关参数）'''
    
    # 2022-03-19
    def operfunc(self, skipna = True, **kwargs):
        '''统计函数，参见numpy同名函数'''
        series = self.series
        index = self.index
        data = series._ValidData
        if skipna:
            if data.dtype==object:
                data = data.astype(float)
            statfunc = getattr(np,'nan'+operator)
        else:
            statfunc = getattr(np,operator)
        return series.__class__(
            data = [statfunc(data[index[k]]) for k in index.keys()],
            index = list(index.keys()) if self.group_keys else None,
            dtype = data.dtype,
            name = operator,
            auto_expand = series._AutoExpand,
            expand_count = series._ExpandCount,
            expand_ratio = series._ExpandRatio,
        )
    
    return operfunc

# 2.2.4 数据表

# 2022-04-03
def CumNAStatFuncFrame(operator, attr = '_ValidData'):
    '''数据表统计函数'''
    
    # 2022-03-13
    def operfunc(self, columns = None, axis = 0, skipna = True, **kwargs):
        '''统计函数，参见numpy同名函数'''
        data = getattr(self,attr)
        if not columns is None and not axis is None:
            if IsSingleType(columns):
                columns = [columns]
            if axis==0:
                cpos = self.columns[columns]
                data = data[:,cpos]
                columns = self.columns.take(cpos)
            else:
                ipos = self.index[columns]
                data = data[ipos]
                columns = self.index.take(ipos)
        if skipna:
            if data.dtype==object:
                data = data.astype(float)
            rt = getattr(np,'nan'+operator)(data,axis,**kwargs)
        else:
            rt = getattr(np,operator)(data,axis,**kwargs)
        
        if axis is None:
            return rt
        elif axis==0:
            return self.__class__(
                data = rt,
                index = self.index,
                columns = self.columns if columns is None else columns,
                dtype = rt.dtype,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        else:
            return self.__class__(
                data = rt,
                index = self.index if columns is None else columns,
                columns = self.columns,
                dtype = rt.dtype,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
    
    return operfunc

# 2022-03-12
def NAStatFuncFrame(operator, attr = '_ValidData'):
    '''数据表统计函数'''
    
    # 2022-03-13
    def operfunc(self, columns = None, axis = 0, skipna = True, **kwargs):
        '''统计函数，参见numpy同名函数'''
        data = getattr(self,attr)
        if not columns is None and not axis is None:
            if IsSingleType(columns):
                columns = [columns]
            if axis==0:
                cpos = self.columns[columns]
                data = data[:,cpos]
                columns = self.columns.take(cpos)
            else:
                ipos = self.index[columns]
                data = data[ipos]
                columns = self.index.take(ipos)
        if skipna:
            if data.dtype==object:
                data = data.astype(float)
            rt = getattr(np,'nan'+operator)(data,axis,**kwargs)
        else:
            rt = getattr(np,operator)(data,axis,**kwargs)
        if axis is None:
            return rt
        else:
            return self.new_aggr_data(rt,axis,operator,columns=columns)
    
    return operfunc

# 2.2.5 数据表分组

# 2022-04-03
def NAStatFuncFrameGroupBy(operator):
    '''数据表分组统计函数'''
    
    # 2022-04-03
    def operfunc(self, columns = None, skipna = True, **kwargs):
        '''统计函数，参见numpy同名函数'''
        axis = self.axis
        frame = self.frame
        data = frame._ValidData
        locIndex = self.index
        locColumns = self.columns
        
        if columns is None:
            if axis==0:
                rtcolumns, rtcol_index = frame.new_columns(False,locColumns)
            else:
                rtindex, rtindex_cols = frame.new_index(False,locIndex)
        else:
            if IsSingleType(columns):
                columns = [columns]
            if axis==0:
                cpos = locColumns[columns]
                data = data[:,cpos]
                rtcolumns = locColumns.take(cpos)
                rtcol_index = None
            else:
                ipos = locIndex[columns]
                data = data[ipos]
                rtindex = locIndex.take(ipos)
                rtindex_cols = None
        
        if skipna:
            if data.dtype==object:
                data = data.astype(float)
            statfunc = getattr(np,'nan'+operator)
        else:
            statfunc = getattr(np,operator)
        
        if axis==0:
            if locIndex.multi_values:
                rtdata = np.array([statfunc(data[p],0) for p in locIndex.pos()])
            else:
                rtdata = np.array(
                    [statfunc(data[[p]],0) for p in locIndex.pos()])
            rtindex = list(locIndex.keys()) if self.group_keys else None
            rtindex_cols = None
        else:
            if locColumns.multi_values:
                rtdata = np.array(
                    [statfunc(data[:,p],1) for p in locColumns.pos()]).T
            else:
                rtdata = np.array(
                    [statfunc(data[:,[p]],1) for p in locColumns.pos()]).T
            rtcolumns = list(locColumns.keys()) if self.group_keys else None
            rtcol_index = None
        return frame.__class__(
            data = rtdata,
            index = rtindex,
            columns = rtcolumns,
            index_cols = rtindex_cols,
            col_index = rtcol_index,
            dtype = data.dtype,
            auto_expand = frame._AutoExpand,
            expand_count = frame._ExpandCount,
            expand_ratio = frame._ExpandRatio,
        )
    
    return operfunc
            

# 3. 其他汇总函数装饰器

# 3.1 基础数据

AggrOperators = {
    'count': len,
    'first': lambda x: x[0],
    'last': lambda x: x[-1],
}
AggrOperatorsSingle = {
    'count': lambda x: np.ones(len(x)),
    'first': lambda x: x,
    'last': lambda x: x,
}

# 3.2 汇总函数装饰器

# 2022-03-20
def AggrFuncSeriesGroupBy(operator):
    '''数据系列分组汇总函数'''
        
    # 2022-03-20
    def operfunc(self):
        '''汇总函数'''
        series = self.series
        index = self.index
        data = series._ValidData
        if index.multi_values:
            aggrfunc = AggrOperators[operator]
            rtdata = [aggrfunc(data[pos]) for pos in index.pos()]
        else:
            rtdata = AggrOperatorsSingle[operator](data[list(index.pos())])
        return series.__class__(
            data = rtdata,
            index = list(index.keys()) if self.group_keys else None,
            dtype = series.dtype,
            name = operator,
            auto_expand = series._AutoExpand,
            expand_count = series._ExpandCount,
            expand_ratio = series._ExpandRatio,
        )
    
    return operfunc

# 4. 二分查找函数装饰器

# 4.1 基础数据

BisectOperators = ['bisect','bisect_left','bisect_right']

# 4.2 二分查找函数装饰器

# 2022-04-03
def BisectFuncSeries(operator, attr = '_ValidData'):
    '''二分查找函数'''
    
    # 2022-04-03
    @tsapply
    def operfunc(self, x, *args, **kwargs):
        '''二分查找，参见bisect同名函数'''
        return getattr(bisect,operator)(getattr(self,attr),x,*args,**kwargs)
    
    return operfunc

# 4. 类装饰器

# 4.1 数据系列

# 4.1.1 数据系列

# 2022-03-20
def DecorateSeries(cls, attr = '_ValidData'):
    '''数据系列类装饰器'''
    cls = OperatorTransfer(cls,attr)
    for op in StatOperators:
        setattr(cls,op,StatFunc(op,attr))
    for op in NAStatOperators:
        setattr(cls,op,NAStatFuncSeries(op,attr))
    for op in CumNAStatOperators:
        setattr(cls,op,CumNAStatFuncSeries(op,attr))
    for op in BisectOperators:
        setattr(cls,op,BisectFuncSeries(op,attr))
    return cls

# 4.1.2 数据系列分组

# 2022-03-20
def DecorateSeriesGroupBy(cls):
    '''数据系列分组类装饰器'''
    for op in NAStatOperators:
        setattr(cls,op,NAStatFuncSeriesGroupBy(op))
    for op in AggrOperators:
        setattr(cls,op,AggrFuncSeriesGroupBy(op))
    return cls

# 4.2 数据表

# 4.2.1 数据表

# 2022-03-20
def DecorateFrame(cls, attr = '_ValidData'):
    '''数据表类装饰器'''
    cls = OperatorTransfer(cls,attr)
    for op in StatOperators:
        setattr(cls,op,StatFunc(op,attr))
    for op in NAStatOperators:
        setattr(cls,op,NAStatFuncFrame(op,attr))
    for op in CumNAStatOperators:
        setattr(cls,op,CumNAStatFuncFrame(op,attr))
    return cls

# 4.2.2 数据表分组

# 2022-04-03
def DecorateFrameGroupBy(cls):
    '''数据表分组类装饰器'''
    for op in NAStatOperators:
        setattr(cls,op,NAStatFuncFrameGroupBy(op))
    return cls
