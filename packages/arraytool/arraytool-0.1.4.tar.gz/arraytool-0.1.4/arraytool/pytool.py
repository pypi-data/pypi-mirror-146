# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 20:22:44 2020

@author: yonder_sky
"""

# Python通用工具库，春秋迭代，yondersky@126.com，2020-11-20
# 更新日期：2022-04-14

import collections, functools, itertools, math, numbers, time
import datetime as dt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from scipy.stats import rankdata

# 0. 全局变量

ConsoleInitStamp = time.strftime('%Y%m%d%H%M%S')
# LogDir = os.getcwd()+'\\Log'
NA = np.nan

# if not os.path.exists(LogDir):
#     os.mkdir(LogDir)

# 1. 系统命令

# 1.1 控制台输出

# 2020-11-20
# def clog(*content, sep = ' ', stdOutput = True):
#     '''
#     控制台输出。
#     【示例】
#     >>> t = clog('pytool',stdOutput=False)
#     >>> leftex(t,8)
#     ' - pytool'
#     '''
#     timeStr = time.strftime('%H:%M:%S')
#     logStr = sep.join((timeStr,'-')+content)
#     if stdOutput:
#         print(logStr)
#     logPath = LogDir+'\\ConsoleLog_'+ConsoleInitStamp+'.txt'
#     with open(logPath,'a') as fp:
#         fp.write(logStr+'\n')
#         fp.close()
#     return logStr

# 2. 通用装饰器

# 2.1 向量化（Apply族）装饰器

'''
【注】（本节通用）
1. 此处apply所指涵义与R语言中的apply系列函数相同，与Python中的apply函数（itertools
   包）不同。
2. 虽然str也为可迭代类型，但通用装饰器不对其展开迭代。
3. 若returnType为None，则返回类型为输入类型（但若输入类型为range，则返回类型为
   list）；否则返回类型为returnType。
'''

# 2.1.1 单参数函数

# 普通函数版本
# 2020-11-22
def emap(func):
    '''
    扩展形式的map函数，返回对应输入的迭代结果。
    【示例】
    >>> emap(abs)(-1)
    1
    >>> emap(abs)(range(5))
    [0, 1, 2, 3, 4]
    >>> emap(abs)([-1,-2,-3],tuple)
    (1, 2, 3)
    '''
    @functools.wraps(func)
    
    # 2020-11-22
    def mapped(iterables, returnType = None):
        if isinstance(iterables,str):
            return func(iterables)
        elif isinstance(iterables,collections.abc.Iterable):
            result = map(func,iterables)
            if returnType is None:
                returnType = type(iterables)
            if returnType is range or returnType is set:
                returnType = list
            if returnType is map:
                return result
            elif returnType is np.ndarray:
                return np.array(list(result))
            elif hasattr(returnType,'values') and hasattr(iterables,'values'):
                return returnType(list(result),iterables.index)
            else:
                return returnType(result)
        else:
            return func(iterables)
    
    return mapped

# 类成员函数版本
# 2021-06-08
def temap(func, returnType = None):
    '''类成员函数版本的emap装饰器'''
    @functools.wraps(func)
    
    # 2021-06-08
    def mapped(self, iterables, returnType = None):
        if isinstance(iterables,str):
            return func(self,iterables)
        elif isinstance(iterables,collections.abc.Iterable):
            result = map(functools.partial(func,self),iterables)
            if returnType is None:
                returnType = type(iterables)
            if returnType is range or returnType is set:
                returnType = list
            if returnType is map:
                return result
            elif returnType is np.ndarray:
                return np.array(list(result))
            elif hasattr(returnType,'values') and hasattr(iterables,'values'):
                return returnType(result,iterables.index)
            else:
                return returnType(result)
        else:
            return func(self,iterables)
    
    return mapped
    
# 2.1.2 多参数函数（向量化首个参数）

# 普通函数版本
# 2020-11-25
def sapply(func, returnType = None):
    '''
    类R语言sapply函数，对首个输入参数向量化。
    【示例】
    >>> sapply(isinstance)('1',int)
    False
    >>> sapply(isinstance)(range(5),bool)
    [False, False, False, False, False]
    >>> sapply(isinstance,tuple)([1,2.2,'abc'],int)
    (True, False, False)
    '''
    @functools.wraps(func)
    
    # 2020-11-25
    def applied(iterables, *args, **kwargs):
        if isinstance(iterables,str):
            return func(iterables,*args,**kwargs)
        elif isinstance(iterables,collections.abc.Iterable):
            result = [func(i,*args,**kwargs) for i in iterables]
            rttype = returnType
            if rttype is None:
                rttype = type(iterables)
            if rttype is range or rttype is set:
                rttype = list
            if rttype is list:
                return result
            elif rttype is np.ndarray:
                return np.array(result)
            elif hasattr(rttype,'values') and hasattr(iterables,'values'):
                return rttype(result,iterables.index)
            else:
                return rttype(result)
        else:
            return func(iterables,*args,**kwargs)
    
    return applied

# 类成员函数版本
# 2022-01-25
def tsapply(func, returnType = None):
    '''类成员函数版本的sapply装饰器'''
    @functools.wraps(func)
    
    # 2022-01-25
    def applied(self, iterables, *args, **kwargs):
        if isinstance(iterables,str):
            return func(self,iterables,*args,**kwargs)
        elif isinstance(iterables,collections.abc.Iterable):
            result = [func(self,i,*args,**kwargs) for i in iterables]
            rttype = returnType
            if rttype is None:
                rttype = type(iterables)
            if rttype is range or rttype is set:
                rttype = list
            if rttype is list:
                return result
            elif rttype is np.ndarray:
                return np.array(result)
            elif hasattr(rttype,'values') and hasattr(iterables,'values'):
                return rttype(result,iterables.index)
            else:
                return rttype(result)
        else:
            return func(self,iterables,*args,**kwargs)
    
    return applied

# 2.1.3 多参数函数（向量化全部无名称参数）

# 普通函数版本
# 2021-12-18
def fapply(func, returnType = None):
    '''
    类R语言fapply函数，对全部无名称输入参数向量化。
    【注】
    1. 所有无名称的输入参数都会被向量化，这些输入参数的长度应相等，否则超过最短长度的
       参数无效；所有不参与向量化的参数均必须显示地注明名称；
    2. 如未指定returnType，以首个参数的类型作为返回值的类型。
    【示例】
    >>> fapply(left)(['pytool','arraytool'],(2,5))
    ['py', 'array']
    >>> fapply(right)('pytool',4)
    'tool'
    >>> fapply(leftex)(['pytool','PyCharm'],count=2)
    ['tool', 'Charm']
    '''
    @functools.wraps(func)
    
    # 2021-12-18
    def applied(*iterables, **kwargs):
        iterable = True
        for i in iterables:
            if IsSingleType(i):
                iterable = False
                break
        if iterable:
            result = [func(*zipi,**kwargs) for zipi in zip(*iterables)]
            rttype = returnType
            if rttype is None:
                rttype = type(iterables[0])
            if rttype is range or rttype is set:
                rttype = list
            if rttype is list:
                return result
            elif rttype is np.ndarray:
                return np.array(result)
            elif hasattr(rttype,'values') and hasattr(iterables[0],'values'):
                return rttype(result,iterables[0].index)
            else:
                return rttype(result)
        else:
            return func(*iterables,**kwargs)
    
    return applied

# 类成员函数版本
# 2022-04-06
def tfapply(func, returnType = None):
    '''类成员函数版本的fapply装饰器'''
    @functools.wraps(func)
    
    # 2022-04-06
    def applied(self, *iterables, **kwargs):
        iterable = True
        for i in iterables:
            if IsSingleType(i):
                iterable = False
                break
        if iterable:
            result = [func(self,*zipi,**kwargs) for zipi in zip(*iterables)]
            rttype = returnType
            if rttype is None:
                rttype = type(iterables[0])
            if rttype is range or rttype is set:
                rttype = list
            if rttype is list:
                return result
            elif rttype is np.ndarray:
                return np.array(result)
            elif hasattr(rttype,'values') and hasattr(iterables[0],'values'):
                return rttype(result,iterable[0].index)
            else:
                return rttype(result)
        else:
            return func(self,*iterables,**kwargs)

# 3. 格式转换

# 3.1 字符串相关

# 3.1.1 子字符串

# 2020-11-20
@sapply
def left(thestr, count):
    '''
    返回thestr前count个字符。
    【示例】
    >>> left(['pytool','arraytool'],2)
    ['py', 'ar']
    '''
    return thestr[:count]

# 2020-11-20
@sapply
def leftex(thestr, count):
    '''
    返回thestr除前count个字符以外的剩余字符。
    【示例】
    >>> leftex(['pytool','arraytool'],2)
    ['tool', 'raytool']
    '''
    return thestr[count:]

# 2021-09-11
@sapply
def mid(thestr, start, count):
    '''
    返回thestr第start个位置开始的count个字符。
    【示例】
    >>> mid(['pytool','arraytool'],3,4)
    ['tool', 'rayt']
    '''
    return thestr[(start-1):(start+count-1)]

# 2021-09-11
@sapply
def right(thestr, count):
    '''
    返回thestr右侧count个字符。
    【示例】
    >>> right(['pytool', 'arraytool'], 4)
    ['tool', 'tool']
    '''
    return thestr[-count:]

# 2021-09-11
@sapply
def rightex(thestr, count):
    '''
    返回thestr除去右侧count个以外的剩余字符。
    【示例】
    >>> rightex(['pytool', 'arraytool'], 4)
    ['py', 'array']
    '''
    return thestr[:-count]


# 3.1.2 字符串转换

# 2021-09-15
@emap
def StrToFloat(numstr):
    '''
    字符串转浮点数（支持百分号）。
    【示例】
    >>> StrToFloat(['33', '33.33', '33.33%'])
    [33.0, 33.33, 0.3333]
    '''
    if numstr[len(numstr)-1]=='%':
        return float(numstr[:-1])/100
    else:
        return float(numstr)

# 3.1.3 字符串添加引用

rquotes = {
    '(': ')',
    '[': ']',
    '{': '}',
    '（': '）',
    '【': '】',
}

# 2022-01-11
@sapply
def ref(refStr, quote = "'"):
    '''
    字符串添加引用。
    【示例】
    >>> ref(['pytool','arraytool'])
    ["'pytool'", "'arraytool'"]
    >>> ref('pytool','"')
    '"pytool"'
    >>> ref('pytool','(')
    '(pytool)'
    >>> ref('pytool','[')
    '[pytool]'
    '''
    rq = rquotes[quote] if quote in rquotes else quote
    return quote+refStr+rq

# 3.1.4 整数转字符串

# 2022-01-11
@sapply
def DateIntToStr(dateInt):
    '''
    数字日期转字符串。
    【示例】
    >>> DateIntToStr([20090101,20121031,0])
    ['2009-01-01', '2012-10-31', '0-00-00']
    '''
    s = '{:05d}'.format(dateInt)
    return s[:-4]+'-'+s[-4:-2]+'-'+s[-2:]

# 3.1.5 当前时间

# 2022-01-24
def CurrentTimeStr():
    '''当前时间戳'''
    return time.strftime('%Y-%m-%d %H:%M:%S')

# 3.1.6 可迭代对象转字符串

# 2022-04-14
def ListToStr(iterables, sep = ',', unique = False, NAIgnored = False):
    '''
    可迭代对象转字符串。

    示例：
    >>> ListToStr([1,2,3],';')
    '1;2;3'
    >>> ListToStr(Series([1,3,2,3,2,1]),unique=True)
    '1,3,2'
    >>> ListToStr('abc')
    'abc'
    >>> ListToStr(['a','b',NA,'c'])
    'a,b,NA,c'
    >>> ListToStr(['a','b',NA,'c'],NAIgnored=True)
    'a,b,c'
    >>> ListToStr({'a':'aa','b':'bb'})
    'aa,bb'
    '''
    values = Series(iterables)
    if unique:
        values = values.drop_duplicates()
    if NAIgnored:
        values = values.dropna()
    else:
        values = values.replace(np.nan,'NA')
    return sep.join(values.astype(str))

# 3.2 数字相关

# 3.2.1 舍入

# 2021-10-17
@emap
def ExactInt(x):
    '''
    舍入取整。

    示例：
    >>> ExactInt([0, 1, 0.5])
    [0, 1, 1]
    '''
    return int(x+0.5)

# 2021-09-14
@sapply
def ExactRound(number, ndigits = 0):
    '''
    自定义舍入函数。
    【示例】
    >>> ExactRound([0, 0.05, 0.0499], 1)
    [0.0, 0.1, 0.0]
    >>> ExactRound(12345.6789,3)
    12345.679
    >>> ExactRound(12345.6789,-3)
    12000.0
    '''
    base = 10**ndigits
    return int(number*base+0.5)/base

# 3.3 切片相关

# 格式化切片
# 2020-11-28
def FormatSlice(s, maxlen):
    '''
    根据输入的最大长度格式化切片。
    【示例】
    >>> FormatSlice(slice(None,None,None),10)
    slice(0, 10, 1)
    >>> FormatSlice(slice(None,None,-1),10)
    slice(10, 0, -1)
    >>> FormatSlice(slice(-3,None,None),10)
    slice(7, 10, 1)
    >>> FormatSlice(slice(2,-2,2),10)
    slice(2, 8, 2)
    '''
    step = 1 if s.step is None else s.step
    start = (0 if step>0 else maxlen) if s.start is None else s.start
    if start<0:
        start %= maxlen
    stop = (maxlen if step>0 else 0) if s.stop is None else s.stop
    if stop<0:
        stop %= maxlen
    return slice(start,stop,step)

# 3.4 列表相关

# 多维笛卡尔积
# 2021-06-03
def ListProduct(*iterables, order = 'C'):
    '''
    多维笛卡尔积。
    【注】
    关于order参数：
      C - 以行主序进行遍历（C风格）
      F - 以列主序进行遍历（F风格）
    【示例】
    >>> ListProduct(list('abc'),[1,0])
    [['a', 'a', 'b', 'b', 'c', 'c'], [1, 0, 1, 0, 1, 0]]
    >>> ListProduct(list('abc'),[1,0],order='F')
    [['a', 'b', 'c', 'a', 'b', 'c'], [1, 1, 1, 0, 0, 0]]
    '''
    if order=='F':
        return [list(z) for z in zip(*itertools.product(*iterables[::-1]))][::-1]
    else:
        return [list(z) for z in zip(*itertools.product(*iterables))]

# 3.5 元组相关

# 多维笛卡尔积
# 2021-06-03
def TupleProduct(*iterables, order = 'C'):
    '''
    多维笛卡尔积。
    【注】
    关于order参数：
      C - 以行主序进行遍历（C风格）
      F - 以列主序进行遍历（F风格）
    【示例】
    >>> TupleProduct(list('abc'),[1,0])
    (('a', 'a', 'b', 'b', 'c', 'c'), (1, 0, 1, 0, 1, 0))
    >>> TupleProduct(list('abc'),[1,0],order='F')
    (('a', 'b', 'c', 'a', 'b', 'c'), (1, 1, 1, 0, 0, 0))
    '''
    if order=='F':
        return tuple(tuple(z) for z in 
            zip(*itertools.product(*iterables[::-1])))[::-1]
    else:
        return tuple(tuple(z) for z in zip(*itertools.product(*iterables)))

# 3.6 日期相关

# 3.6.1 日期转数字

# 2022-01-07
@emap
def DateToInt(date):
    '''
    日期转数字。
    【示例】
    >>> DateToInt([dt.date(2021,4,1),dt.date(2021,4,11)])
    [20210401, 20210411]
    '''
    if date is None:
        return date
    else:
        return date.year*10000+date.month*100+date.day

# 3.6.2 数字转日期

# 2022-01-18
@emap
def IntToDate(dateInt):
    '''
    数字转日期。
    【示例】
    >>> IntToDate([20220101,20220111])
    [datetime.date(2022, 1, 1), datetime.date(2022, 1, 11)]
    '''
    if dateInt is None:
        return dateInt
    dateInt = int(dateInt)
    return dt.date(dateInt//10000,dateInt%10000//100,dateInt%100)

# 3.6.3 日期扩展函数

# 3.6.3.1 闰年判断

# 2022-01-17
def IsLeapYearSingle(year):
    '''
    判断指定年份是否为闰年。
    【示例】
    >>> IsLeapYear([1900,1950,2000,2008])
    [False, False, True, True]
    '''
    return True if year%400==0 or year%4==0 and year%100!=0 else False

IsLeapYear = emap(IsLeapYearSingle)

# 3.6.3.2 年月天数

MonthDaysDict = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

# 2022-01-17
def monthdaysSingle(year, month):
    '''
    返回对应年月当月天数。
    【示例】
    >>> monthdays([1900,1950,2000,2008],[2,2,2,2])
    [28, 28, 29, 29]
    >>> monthdays([2022,2023,2024],[5,8,11])
    [31, 31, 30]
    '''
    return 29 if IsLeapYearSingle(year) and month==2 else MonthDaysDict[month]

monthdays = fapply(monthdaysSingle)

# 3.6.3.3 月份偏离

# 月份偏移
# 2022-01-18
@sapply
def edate(date, count = 1):
    '''
    返回指定日期前推/后推一定月份的日期。
    【示例】
    >>> edate([20220131,20220228,20200131,20200229])
    [20220228, 20220328, 20200229, 20200329]
    >>> edate([20220131,20201230],-1)
    [20211231, 20201130]
    >>> edate([dt.date(2022,1,31),dt.date(2022,2,28)])
    [datetime.date(2022, 2, 28), datetime.date(2022, 3, 28)]
    >>> edate([dt.date(2022,3,31),dt.date(2021,12,30)])
    [datetime.date(2022, 4, 30), datetime.date(2022, 1, 30)]
    >>> edate(pd.Timestamp('2022-01-01 19:31:31'))
    Timestamp('2022-02-01 19:31:31')
    '''
    if IsNA(date):
        return NA
    elif isinstance(date,numbers.Real):
        return edateIntSingle(int(date),count)
    else:
        return edateDateSingle(date,count)

# 普通日期版本
# 2022-01-18
def edateDateSingle(date, count = 1):
    '''
    返回指定日期前推/后推一定月份的日期。
    '''
    year = date.year
    month = date.month
    day = date.day
    
    month += count
    if month>12:
        year += month//12
        month %= 12
    elif month<1:
        year += (month-1)//12
        month = (month-1)%12+1
    day = min(day,monthdaysSingle(year,month))
    offset = dt.date(year,month,day)-dt.date(date.year,date.month,date.day)
    return date+offset

# 数字日期版本
# 2022-01-17
def edateIntSingle(dateInt, count = 1):
    '''
    返回指定日前推/后推一定月份的日期。
    '''
    year = dateInt//10000
    month = dateInt%10000//100
    day = dateInt%100
    
    month += count
    if month>12:
        year += month//12
        month %= 12
    elif month<1:
        year += (month-1)//12
        month = (month-1)%12+1
    day = min(day,monthdaysSingle(year,month))
    return year*10000+month*100+day

# 3.6.3.4 区间起止日

# 年起始日
# 2022-01-17
@emap
def StartOfTheYear(date):
    '''
    返回指定日所在年起始日。
    【示例】
    >>> StartOfTheYear([20211231,dt.date(2020,12,1)])
    [20210101, datetime.date(2020, 1, 1)]
    '''
    if IsNASingle(date):
        return NA
    elif isinstance(date,numbers.Real):
        return int(date)//10000*10000+101
    else:
        return dt.date(date.year,1,1)

# 年结束日
# 2022-01-18
@emap
def EndOfTheYear(date):
    '''
    返回指定日所在年结束日。
    【示例】
    >>> EndOfTheYear([20210101,dt.date(2021,10,1)])
    [20211231, datetime.date(2021, 12, 31)]
    '''
    if IsNASingle(date):
        return NA
    elif isinstance(date,numbers.Real):
        return int(date)//10000*10000+1231
    else:
        return dt.date(date.year,12,31)

# 季起始日
# 2022-01-18
@emap
def StartOfTheQuarter(date):
    '''
    返回指定日所在季度起始日。
    【示例】
    >>> StartOfTheQuarter([20211231,dt.date(2021,9,30)])
    [20211001, datetime.date(2021, 7, 1)]
    '''
    if IsNASingle(date):
        return NA
    if isinstance(date,numbers.Real):
        date = int(date)
        m = date%10000//100
        return date//10000*10000+(m-(m+2)%3)*100+1 
    else:
        m = date.month
        return dt.date(date.year,m-(m+2)%3,1)

# 季结束日
# 2022-01-19
@emap
def EndOfTheQuarter(date):
    '''
    返回指定日所在季度结束日。
    【示例】
    >>> EndOfTheQuarter([20211001,dt.date(2022,1,11)])
    [20211231, datetime.date(2022, 3, 31)]
    '''
    if IsNASingle(date):
        return NA
    if isinstance(date,numbers.Real):
        date = int(date)
        y = date//10000
        m = date%10000//100
        m = m+2-(m+2)%3
        return y*10000+m*100+monthdaysSingle(y,m)
    else:
        y = date.year
        m = date.month
        m = m+2-(m+2)%3
        return dt.date(y,m,monthdaysSingle(y,m))

# 月起始日
# 2022-01-18
@emap
def StartOfTheMonth(date):
    '''
    返回指定日所在月份起始日。
    【示例】
    >>> StartOfTheMonth([dt.date(2011,12,31),20110430])
    [datetime.date(2011, 12, 1), 20110401]
    '''
    if IsNASingle(date):
        return NA
    if isinstance(date,numbers.Real):
        date = int(date)
        return date//10000*10000+date%10000//100*100+1
    else:
        return dt.date(date.year,date.month,1)

# 月结束日
# 2022-01-18
@emap
def EndOfTheMonth(date):
    '''
    返回指定日所在月份结束日。
    【示例】
    >>> EndOfTheMonth([20210201,dt.date(2022,1,1)])
    [20210228, datetime.date(2022, 1, 31)]
    '''
    if IsNASingle(date):
        return NA
    if isinstance(date,numbers.Real):
        date = int(date)
        y = date//10000
        m = date%10000//100
        return y*10000+m*100+monthdaysSingle(y,m)
    else:
        y = date.year
        m = date.month
        return dt.date(y,m,monthdaysSingle(y,m))

# 周起始日
# 2022-01-18
@sapply
def StartOfTheWeek(date, weekStart = 1):
    '''
    返回指定日所在周起始日。
    【注】weekStart参数指周起始日期，周一至周六分别取1至6，周日可取0或7。
    【示例】
    >>> StartOfTheWeek([20220115,20220116,20220117])
    [20220110, 20220110, 20220117]
    >>> StartOfTheWeek([20220115,20220116,20220117],0)
    [20220109, 20220116, 20220116]
    '''
    if IsNASingle(date):
        return NA
    if isinstance(date,numbers.Real):
        dateInt = True
        date = IntToDate(int(date))
    else:
        dateInt = False
    start = date-dt.timedelta((date.weekday()-weekStart+1)%7)
    return DateToInt(start) if dateInt else start

# 周结束日
# 2022-01-18
@sapply
def EndOfTheWeek(date, weekStart = 1):
    '''
    返回指定日所在周结束日。
    【注】weekStart参数指周周起始日期，周一至周六分别取1至6，周日可取0或7。
    【示例】
    >>> EndOfTheWeek([20220115,20220116,20220117])
    [20220116, 20220116, 20220123]
    >>> EndOfTheWeek([20220115,20220116,20220117],0)
    [20220115, 20220122, 20220122]
    '''
    if IsNASingle(date):
        return NA
    if isinstance(date,numbers.Real):
        dateInt = True
        date = IntToDate(int(date))
    else:
        dateInt = False
    end = date+dt.timedelta((-date.weekday()+weekStart-2)%7)
    return DateToInt(end) if dateInt else end

# 3.6.3.5 日期间隔

# 2022-04-02
def DateDiff(startDate, endDate):
    '''
    日期间隔。
    【示例】
    >>> DateDiff(20220101,20220331)
    89
    '''
    if IsInteger(startDate):
        startDate = IntToDate(startDate)
    if IsInteger(endDate):
        endDate = IntToDate(endDate)
    return (endDate-startDate).days

# 4. 类型判断

# 4.1 变量类型判断

# 2021-02-16
def IsArray(var):
    '''
    判断是否为numpy.ndarray类型对象。
    【示例】
    >>> IsArray(np.ones(10))
    True
    '''
    return True if isinstance(var,np.ndarray) else False

# 2020-11-28
def IsBool(var):
    '''
    判断是否为bool类型（包括常规bool类型及numpy中的bool类型）对象。
    【示例】
    >>> IsBool(False)
    True
    >>> IsBool(np.sin(1)<0)
    True
    >>> IsBool('a')
    False
    '''
    return True if isinstance(var,np.bool_) or isinstance(var,bool) else False

# 2021-08-12
def IsDataFrame(var):
    '''
    判断是否为DataFrame。
    【示例】
    >>> IsDataFrame(DataFrame())
    True
    >>> IsDataFrame(1)
    False
    '''
    return True if isinstance(var,DataFrame) else False

# 2022-01-25
def IsDateInt(var):
    '''
    判断是否为数字日期。
    '''
    return False if IsNASingle(var) else isinstance(var,numbers.Real)

# 2021-10-06
def IsIndex(var):
    '''
    判断是否为pandas索引。
    '''
    return True if isinstance(var,pd.Index) else False

# 2020-11-28
def IsInteger(var):
    '''
    判断是否为整数。
    【示例】
    >>> IsInteger(1)
    True
    >>> IsInteger([])
    False
    '''
    return True if isinstance(var,numbers.Integral) else False

# 2021-06-08
def IsIterable(var):
    '''
    判断是否为可迭代类型对象。
    【示例】
    >>> IsIterable([])
    True
    >>> IsIterable(())
    True
    >>> IsIterable(np.arange(3))
    True
    >>> IsIterable(range(3))
    True
    >>> IsIterable(slice(3))
    False
    '''
    return True if isinstance(var,collections.abc.Iterable) else False

# 2021-10-06
def IsMultiIndex(var):
    '''
    判断是否为pandas多重索引。
    【示例】
    >>> ser1 = Series(range(4))
    >>> IsMultiIndex(ser1.index)
    False
    >>> ser2 = Series(range(4),[list('abcd'),list('AAAB')])
    >>> IsMultiIndex(ser2.index)
    True
    '''
    return True if isinstance(var,pd.MultiIndex) else False

# 2021-05-13
def IsSeries(var):
    '''
    判断是否为pandas系列。
    【示例】
    >>> IsSeries(Series(range(5)))
    True
    >>> IsSeries(range(5))
    False
    '''
    return True if isinstance(var,Series) else False

# 2021-05-14
def IsSimpleIndex(var):
    '''
    判断是否为可化简的索引类型（索引为RangeIndex对象且start为0）。
    【示例】
    >>> ser1 = Series(range(4))
    >>> IsSimpleIndex(ser1.index)
    True
    >>> ser2 = Series(range(4),range(1,5))
    >>> IsSimpleIndex(ser2.index)
    False
    >>> ser3 = Series(range(4),list('abcd'))
    >>> IsSimpleIndex(ser3.index)
    False
    '''
    return var.start==0 if isinstance(var,pd.RangeIndex) else False

# 2020-11-28
def IsSingleType(var):
    '''
    判断是否为单值类型（不可迭代类型或str）。
    【示例】
    >>> IsSingleType(1)
    True
    >>> IsSingleType(NA)
    True
    >>> IsSingleType([1,4])
    False
    >>> IsSingleType(range(5))
    False
    >>> IsSingleType(slice(None,None,None))
    False
    '''
    if not isinstance(var,str) and hasattr(var,'__iter__') \
        or isinstance(var,slice):
        return False
    else:
        return True

# 2021-07-10
def IsSingleType2(var):
    '''
    判断是否为单值类型。
    【注】IsSingleType2函数slice对象返回True，其余返回与IsSingleType函数相同。
    【示例】
    >>> IsSingleType2(1)
    True
    >>> IsSingleType2(range(5))
    False
    >>> IsSingleType2(slice(None,None,None))
    True
    '''
    if not isinstance(var,str) and hasattr(var,'__iter__'):
        return False
    else:
        return True

# 2021-02-14
def IsSlice(var):
    '''
    判断是否为切片。
    【示例】
    >>> IsSlice(slice(10))
    True
    >>> IsSlice(10)
    False
    '''
    return True if isinstance(var,slice) else False

# 2022-01-18
def IsTimestamp(var):
    '''
    判断是否为Timestamp。
    【示例】
    >>> IsTimestamp(pd.Timestamp('2022-01-01'))
    True
    >>> IsTimestamp('None')
    False
    '''
    return True if isinstance(var,pd.Timestamp) else False

# 4.2 NA判定

# 2021-10-14
def IsNA(value):
    '''
    是否NA（即np.nan）。
    注：直接使用np.isnan无法处理输入非实数的情况。

    示例：
    >>> IsNA([np.nan, 0, 1.2, 'pyTool'])
    [True, False, False, False]
    '''
    if IsSeries(value) or IsDataFrame(value):
        return value.isnull()
    return IsNAFull(value)

# 2021-10-14
def IsNASingle(value):
    if value is None:
        return True
    elif isinstance(value,numbers.Real):
        return np.isnan(value)
    else:
        return False

IsNAFull = emap(IsNASingle)

# 5. 数据分析

# 5.1 长度自适应

# 2020-11-28
def ExpandSize(curLen, targetLen, expandCount, expandRatio):
    '''
    返回扩张后的维度大小。
    【示例】
    >>> ExpandSize(27,None,10,2)
    37
    >>> ExpandSize(27,1000,10,2)
    1007
    >>> ExpandSize(27,None,0,2)
    54
    >>> ExpandSize(27,1000,0,2)
    1728
    '''
    rtlen = curLen
    if expandCount==0:
        # 比例扩张
        rtlen = max(math.ceil(rtlen*expandRatio),rtlen+1)
        if not targetLen is None:
            while rtlen<targetLen:
                rtlen = max(math.ceil(rtlen*expandRatio),rtlen+1)
    else:
        # 数量扩张
        rtlen += expandCount
        if not targetLen is None:
            while rtlen<targetLen:
                rtlen += expandCount
    return rtlen

# 5.2 排序

# 5.2.1 排名

# 2021-10-14
def rank(x, ascending = True, na_option = 'keep', method = 'average'):
    '''
    排名。

    【注】
    1. ascending、na_option、method参数请参见DataFrame.rank函数对应同名参数的帮助。
    2. method参数除first参数，新增参数last（相同值依次倒序排名）。

    【示例】
    >>> l = [2,2,NA,1,1,1,NA,2,2,3]
    >>> rank(l,method='average')
    array([5.5, 5.5, nan, 2. , 2. , 2. , nan, 5.5, 5.5, 8. ])
    >>> rank(l,method='min')
    array([ 4.,  4., nan,  1.,  1.,  1., nan,  4.,  4.,  8.])
    >>> rank(l,method='max')
    array([ 7.,  7., nan,  3.,  3.,  3., nan,  7.,  7.,  8.])
    >>> rank(l,method='dense')
    array([ 2.,  2., nan,  1.,  1.,  1., nan,  2.,  2.,  3.])
    >>> rank(l,method='first')
    array([ 4.,  5., nan,  1.,  2.,  3., nan,  6.,  7.,  8.])
    >>> rank(l,method='last')
    array([ 7.,  6., nan,  3.,  2.,  1., nan,  5.,  4.,  8.])
    >>> rank(l,ascending=False,method='average')
    array([3.5, 3.5, nan, 7. , 7. , 7. , nan, 3.5, 3.5, 1. ])
    >>> rank(l,ascending=False,method='min')
    array([ 2.,  2., nan,  6.,  6.,  6., nan,  2.,  2.,  1.])
    >>> rank(l,ascending=False,method='max')
    array([ 5.,  5., nan,  8.,  8.,  8., nan,  5.,  5.,  1.])
    >>> rank(l,ascending=False,method='dense')
    array([ 2.,  2., nan,  3.,  3.,  3., nan,  2.,  2.,  1.])
    >>> rank(l,ascending=False,method='first')
    array([ 2.,  3., nan,  6.,  7.,  8., nan,  4.,  5.,  1.])
    >>> rank(l,ascending=False,method='first',na_option='top')
    array([ 4.,  5.,  1.,  8.,  9., 10.,  2.,  6.,  7.,  3.])
    >>> rank(l,ascending=False,method='first',na_option='bottom')
    array([ 2.,  3.,  9.,  6.,  7.,  8., 10.,  4.,  5.,  1.])
    >>> rank(l,ascending=False,method='last')
    array([ 5.,  4., nan,  8.,  7.,  6., nan,  3.,  2.,  1.])
    >>> rank(l,ascending=False,method='last',na_option='top')
    array([ 7.,  6.,  2., 10.,  9.,  8.,  1.,  5.,  4.,  3.])
    >>> rank(l,ascending=False,method='last',na_option='bottom')
    array([ 5.,  4., 10.,  8.,  7.,  6.,  9.,  3.,  2.,  1.])
    '''
    inverse = ascending and method=='last' or not ascending and method=='first'
    rmethod = method
    if method=='first' or method=='last':
        rmethod = 'ordinal'
    if not ascending:
        if method=='max':
            rmethod = 'min'
        elif method=='min':
            rmethod = 'max'

    xlen = len(x)
    napos = [i for i in range(xlen) if IsNASingle(x[i])]
    nalen = len(napos)
    if nalen==0:
        xrank = rankdata(x[::-1],rmethod)[::-1] if inverse \
            else rankdata(x,rmethod)
        if ascending:
            return xrank
        else:
            maxrank = xrank.max()+1 if method=='dense' else xlen+1
            return maxrank-xrank
    elif nalen==xlen:
        if na_option=='keep':
            return x if IsArray(x) else np.array(x)
        elif method=='average':
            return np.repeat(xlen/2,xlen)
        elif method=='min' or method=='dense':
            return np.repeat(1,xlen)
        elif method=='max':
            return np.repeat(xlen,xlen)
        elif method=='first':
            return np.arange(1,xlen+1)
        elif method=='last':
            return np.arange(xlen,0,-1)
    else:
        xrank = np.repeat(NA,xlen)
        nnapos = list(set(range(xlen))-set(napos))
        nnalen = len(nnapos)
        xvalue = x[nnapos] if IsArray(x) else [x[p] for p in nnapos]
        if inverse:
            xvalue = xvalue[::-1]
        xrank[nnapos] = rankdata(xvalue,rmethod)
        if inverse:
            xrank[nnapos] = xrank[nnapos[::-1]]
        maxrank = xrank[nnapos].max()+1 if method=='dense' else nnalen+1
        if not ascending:
            xrank[nnapos] = maxrank-xrank[nnapos]
        if na_option=='top' or na_option=='first':
            if method=='dense':
                xrank[nnapos] += 1
                xrank[napos] = 1
            else:
                xrank[nnapos] += nalen
                if method=='average':
                    xrank[napos] = nalen/2
                elif method=='min':
                    xrank[napos] = 1
                elif method=='max':
                    xrank[napos] = nalen
                elif method=='first':
                    xrank[napos] = np.arange(1,nalen+1)
                elif method=='last':
                    xrank[napos] = np.arange(nalen,0,-1)
        elif na_option=='bottom' or na_option=='last':
            if method=='min' or method=='dense':
                xrank[napos] = maxrank
            elif method=='average':
                xrank[napos] = (maxrank+xlen)/2
            elif method=='max':
                xrank[napos] = xlen
            elif method=='first':
                xrank[napos] = np.arange(maxrank,maxrank+nalen)
            elif method=='last':
                xrank[napos] = np.arange(xlen,xlen-nalen,-1)
        return xrank

# 5.2.2 百分比排名

# 2021-10-14
def PercentRank(x, ascending = True, na_option = 'keep',  method = 'average',
     na_default = 0.5, bound_method = 'mid'):
    '''
    百分比排名。
    【注】
    1. ascending、na_option、method参数请参见rank函数对应同名参数的帮助；
    2. 仅当na_option参数取值为keep时，na_default参数可用，将排名后的NA值以
       na_default替换；
    3. bound_method参数代表边界处理方式，取值如下：
      exc - 极值在边界
      inc - 极值在边界内一区间
      mid - 极值在边界内中点处
    【示例】
    >>> PercentRank([1,2,3,NA,5])
    array([0.125, 0.375, 0.625, 0.5  , 0.875])
    >>> PercentRank([1,2,3,NA,5],bound_method='exc')
    array([0.        , 0.33333333, 0.66666667, 0.5       , 1.        ])
    >>> PercentRank([1,2,3,NA,5],bound_method='inc')
    array([0.2, 0.4, 0.6, 0.5, 0.8])
    '''
    rt = rank(x,ascending,na_option,method)
    napos = which(np.isnan(rt))
    clen = len(rt)-len(napos) if na_option=='keep' else len(rt)
    if clen>1:
        if bound_method=='exc':
            rt = (rt-1)/(clen-1)
        elif bound_method=='inc':
            rt/= (clen+1)
        else:
            rt = (rt-0.5)/clen
    if na_option=='keep' and not np.isnan(na_default):
        rt[napos] = na_default
    return rt

# 5.2.3 下标排序

# 5.2.3.1 单序列下标排序

# 2021-11-28
def argsort(x, ascending = True, na_option = 'last', method = 'first', 
    kind = None):
    '''
    单序列下标排序。
    【注】
    1. na_option支持参数：
       keep - 保持原样
       drop/ignore - 不保留NA
       last/bottom - 置于最后
       first/top - 置于最前
    2. method（相同值处理）支持参数：
       first - 同值正序在前
       last - 同值倒序在前
    3. 返回值为int64类型的numpy数组，当na_option为keep，NA位置返回的下标为-1。
    【示例】
    >>> l = [2,2,NA,1,1,1,NA,2,2,3]
    >>> argsort(l)
    array([3, 4, 5, 0, 1, 7, 8, 9, 2, 6], dtype=int64)
    >>> argsort(l,method='last')
    array([5, 4, 3, 8, 7, 1, 0, 9, 6, 2], dtype=int64)
    >>> argsort(l,False)
    array([9, 0, 1, 7, 8, 3, 4, 5, 2, 6], dtype=int64)
    >>> argsort(l,False,method='last')
    array([9, 8, 7, 1, 0, 5, 4, 3, 6, 2], dtype=int64)
    >>> argsort(l,False,na_option='first',method='last')
    array([6, 2, 9, 8, 7, 1, 0, 5, 4, 3], dtype=int64)
    >>> argsort(l,False,na_option='ignore',method='last')
    array([9, 8, 7, 1, 0, 5, 4, 3], dtype=int64)
    >>> argsort(l,False,na_option='keep',method='last')
    array([ 9,  8, -1,  7,  1,  0, -1,  5,  4,  3], dtype=int64)
    '''
    isArr = IsArray(x)
    if isArr and x.dtype==object:
        # np.argsort不能正确处理dtype为object的情况，暂时需转为list
        x = list(x)
        isArr = False
    
    xlen = len(x)
    if ascending and na_option=='last':
        return np.argsort(x,kind=kind) if method=='first' \
            else xlen-1-np.argsort(x[::-1],kind=kind)
    elif not ascending and na_option=='first':
        return np.argsort(x,kind=kind)[::-1] if method=='last' \
            else (xlen-1-np.argsort(x[::-1],kind=kind))[::-1]
    
    inverse = ascending and method=='last' or not ascending and method=='first'
    napos = [i for i in range(xlen) if IsNASingle(x[i])]
    nalen = len(napos)
    if nalen==0:
        xarg = xlen-1-np.argsort(x[::-1],kind=kind) if inverse \
            else np.argsort(x,kind=kind)
        return xarg if ascending else xarg[::-1]
    elif nalen==xlen:
        if na_option=='keep':
            return x if IsArray(x) else np.array(x)
        else:
            return np.arange(xlen) if method=='first' \
                else np.arange(xlen-1,-1,-1)
    else:
        nnalen = xlen-nalen
        nnapos = np.array(list(set(range(xlen))-set(napos)),dtype=np.int64)
        if isArr:
            nnaarg = nnalen-1-np.argsort(x[nnapos[::-1]],kind=kind) \
                if inverse else np.argsort(x[nnapos],kind=kind)
        else:
            if inverse:
                xvalue = [x[p] for p in nnapos[::-1]]
                nnaarg = nnalen-1-np.argsort(xvalue,kind=kind)
            else:
                xvalue = [x[p] for p in nnapos]
                nnaarg = np.argsort(xvalue,kind=kind)
        nnaarg = nnapos[nnaarg] if ascending else nnapos[nnaarg[::-1]]
        if na_option=='drop' or na_option=='ignore':
            return nnaarg
        else:
            xarg = np.repeat(np.int64(-1),xlen)
            if na_option=='keep':
                xarg[nnapos] = nnaarg
            elif na_option=='first' or na_option=='top':
                xarg[:nalen] = napos[::-1] if method=='last' else napos
                xarg[nalen:] = nnaarg
            else:
                xarg[:nnalen] = nnaarg
                xarg[nnalen:] = napos[::-1] if method=='last' else napos
            return xarg

# 5.2.3.2 多序列下标排序

# 2021-12-13
def LexsortArray(data, ascending = True, na_option = 'last', method = 'first'):
    '''
    多序列下标排序（ndarray类型）。
    '''
    if data.ndim==1:
        return argsort(data,ascending,na_option,method)
    
    rlen, clen = data.shape
    if ascending==True and na_option=='last' and method=='first':
        end = clen-1
        if data.dtype==object:
            return np.lexsort([list(data[:,end-i]) for i in range(clen)])
        else:
            return np.lexsort([data[:,end-i] for i in range(clen)])
    
    base = 1.0
    prank = np.repeat(0.0,rlen)
    ascList = isinstance(ascending,list)
    naList = isinstance(na_option,list)
    for i in range(clen):
        asc = ascending[i] if ascList else ascending
        naop = na_option[i] if naList else na_option
        prank += rank(data[:,i],asc,naop)*base
        base /= rlen
    return argsort(prank,method=method)

# 2021-12-14
def LexsortList(data, ascending = True, na_option = 'last', method = 'first'):
    '''
    多资产下标排序（可迭代类型）。
    '''
    clen = len(data)
    rlen = len(data[0])
    for i in range(1,clen):
        if len(data[i])!=rlen:
            raise ValueError('Column size mismatch.')
    
    # 由于无法确定data各元素是否为dtype为object的ndarray，暂不支持np.lexsort加速。
    # if ascending==True and na_option=='last' and method=='first':
    #     return np.lexsort(data[::-1])
    
    base = 1.0
    prank = np.repeat(0.0,rlen)
    ascList = isinstance(ascending,list)
    naList = isinstance(na_option,list)
    for i in range(clen):
        asc = ascending[i] if ascList else ascending
        naop = na_option[i] if naList else na_option
        prank += rank(data[i],asc,naop)*base
        base /= rlen
    return argsort(prank,method=method)

# 2021-12-09
def lexsort(data, ascending = True, na_option = 'last', method = 'first'):
    '''
    多序列下标排序。
    【注】与np.lexsort相反，在data的遍历中，先遍历到的成员在排序时优先比较。
    【示例】
    >>> l = [2,2,NA,1,1,1,NA,2,2,3]
    >>> l2 = list('aacceffsec')
    >>> lexsort([l,l2])
    array([3, 4, 5, 0, 1, 8, 7, 9, 2, 6], dtype=int64)
    >>> lexsort([l,l2],method='last')
    array([3, 4, 5, 1, 0, 8, 7, 9, 2, 6], dtype=int64)
    >>> lexsort([l,l2],False)
    array([9, 7, 8, 0, 1, 5, 4, 3, 6, 2], dtype=int64)
    >>> lexsort([l,l2],False,method='last')
    array([9, 7, 8, 1, 0, 5, 4, 3, 6, 2], dtype=int64)
    >>> lexsort([l,l2],False,na_option='first',method='last')
    array([6, 2, 9, 7, 8, 1, 0, 5, 4, 3], dtype=int64)
    '''
    if IsArray(data):
        if data.dtype==object:
            return LexsortList([data[:,i] for i in range(len(data.shape[0]))],
                ascending,na_option,method)
        else:
            return LexsortArray(data,ascending,na_option,method)
    else:
        return LexsortList(data,ascending,na_option,method)

# 5.3 集合取补

# 5.3.1 下标取补

# 2022-02-23
def posdiff(size, pos):
    '''
    下标取补。
    【示例】
    >>> posdiff(5,[1,3])
    [0, 2, 4]
    '''
    pos = set(pos)
    return [i for i in range(size) if not i in pos]

# 5.3.2 集合取补

# 2022-02-03
def setdiff(a, b, ordered = True):
    '''
    集合取补（保序）。
    【示例】
    >>> setdiff([5,3,2,4,1],[3,5,2])
    [4, 1]
    >>> setdiff([5,3,2,4,1],[3,5,2],False)
    [1, 4]
    '''
    if ordered:
        a = collections.OrderedDict.fromkeys(a)
        b = set(b)
        return [i for i in a if not i in b]
    else:
        return list(np.setdiff1d(a,b))

# 5.4 增长率计算

# 2022-03-11
def GrowthRate(startValue, endValue):
    '''
    财务增长率。
    【公式】（当期值-上期值）/abs（上期值）
    【示例】
    >>> GrowthRate([2,-1],[-1,2])
    array([-1.5,  3. ])
    '''
    if hasattr(startValue,'_ValidData'):
        startValue = startValue._ValidData
    elif hasattr(startValue,'values'):
        startValue = startValue.values
    elif not IsArray(startValue):
        startValue = np.array(startValue,np.float64)
    if hasattr(endValue,'_ValidData'):
        endValue = endValue._ValidData
    elif hasattr(endValue,'values'):
        endValue = endValue.values
    elif not IsArray(endValue):
        endValue = np.array(endValue,np.float64)
    return (endValue-startValue)/np.abs(startValue)

# 6. 逻辑扩展

# 2021-12-02
def which(expression):
    '''
    下标筛选函数（同R语言which）。
    【示例】
    >>> which(np.arange(5)==4)
    array([4], dtype=int64)
    '''
    return np.where(expression)[0]

if __name__=='__main__':
    import doctest
    doctest.testmod()
