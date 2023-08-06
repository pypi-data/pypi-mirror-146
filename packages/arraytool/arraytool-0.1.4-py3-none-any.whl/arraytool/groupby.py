# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 13:53:35 2022

@author: chenyc
"""

# arraytool包分组模块，春秋迭代，yondersky@126.com，2022-03-20
# 更新日期：2022-03-29

import numpy as np

from arraytool.core import ArraySeries, ArraySeriesLocIndexer
from arraytool.decorator import DecorateSeriesGroupBy
from arraytool.pytool import IsArray, IsSingleType

# 1. 数据序列分组类

# 2022-03-19
@DecorateSeriesGroupBy
class ArraySeriesGroupBy(ArraySeriesLocIndexer):
    '''
    数据序列分组类。
    '''
    
    # 2022-03-19
    def __init__(self, series, values = None, group_keys = True):
        if values is None:
            values = series
        super().__init__(series,values)
        self.group_keys = group_keys
        return
    
    # 2022-03-19
    def apply(self, func, skipna = False, slice_kind = 'array', 
        group_keys = None, *args, **kwargs):
        '''
        自定义汇总函数。
        【参数表】
        func - 汇总函数
        multi_values - 返回值是否为多值
        slice_kind - 切片类型
          Array/array - 切片时传入数组
          Series/series - 切片时传入数据系列
        【注】
        1. func返回值类型必须为简单值、np.ndarray或ArraySeries。
        2. func返回值类型应一致；返回值类型为ArraySeries时，各返回值的索引类型应一致。
        '''
        if isinstance(func,str):
            if hasattr(self,func):
                return getattr(self,func)
            else:
                raise KeyError(
                    'ArraySeriesGroupBy: {} - function not found.'.format(func))
        
        series = self.series
        if skipna:
            series = series.dropna()
        if series.empty:
            return ArraySeries()
        
        slice_kind = slice_kind.lower()
        data = series._ValidData if slice_kind=='array' else series.iloc
        index = self.index
        details = [func(data[p],*args,**kwargs) for p in index.pos()]
        d0 = details[0]
        dsingle = IsSingleType(d0)
        darray = False if dsingle else IsArray(d0)
        if dsingle:
            rtdata = np.array(details)
            multi_values = False
        else:
            if darray:
                rtdata = np.concatenate(details)
            else:
                rtdata = np.concatenate([d._ValidData for d in details])
            dlens = [len(d) for d in details]
            multi_values = max(dlens)>1
        
        if group_keys is None:
            group_keys = self.group_keys
        if group_keys:
            keys = list(index.keys())
            if multi_values:
                rtindex = []
                for i in range(len(keys)):
                    rtindex += [keys[i]]*dlens[i]
            else:
                rtindex = keys
        elif multi_values and not dsingle and not darray \
            and not d0.index.simple:
            rtindex = np.concatenate([d.index.values for d in details])
        else:
            rtindex = None
        
        return ArraySeries(
            data = rtdata,
            index = rtindex,
            dtype = rtdata.dtype,
            auto_expand = series._AutoExpand,
            expand_count = series._ExpandCount,
            expand_ratio = series._ExpandRatio,
        )
