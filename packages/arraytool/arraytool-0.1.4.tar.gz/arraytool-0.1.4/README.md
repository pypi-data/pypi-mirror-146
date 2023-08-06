# arraytool

## 介绍

基于numpy的Series及DataFrame数据结构。

arraytool包中对应于Series及DataFrame的数据类分别为ArraySeries及ArrayFrame，两者同Series及DataFrame之间可方便地进行转换。

## 安装

```python
pip install arraytool
```

## 引入

```python
import arraytool
from arraytool import ArraySeries, ArrayFrame
```

## ArraySeries

### 构造

```python
>>> s1 = ArraySeries(['a','bb','ccc'])
>>> s1
0      a
1     bb
2    ccc
dtype: object
```

### 取值

```python
>>> s1[2]
'ccc'
>>> s1[:2]
0     a
1    bb
dtype: object
```

### 使用索引

```python
>>> s2 = ArraySeries([2,3,4,5],list('aabc'))
>>> s2.iloc[:2]
a    2
a    3
dtype: object
>>> s2.loc['a']
a    2
a    3
dtype: object
>>> s2.loc['b']
4
>>> s2.loc[list('ab')]
a    2
a    3
b    4
dtype: object
```

## ArrayFrame

### 构造

```python
>>> af = ArrayFrame()
>>> af['A'] = list('abcd')
>>> af['B'] = range(4)
>>> af['C'] = [True,True,False,False]
>>> af
   A  B      C
0  a  0   True
1  b  1   True
2  c  2  False
3  d  3  False
```

### 取值

```python
>>> af[list('BC')]
   B      C
0  0   True
1  1   True
2  2  False
3  3  False
```

### 使用索引

#### iloc索引

```python
>>> af.iloc[0,0]
'a'
>>> af.iloc[0]
   A  B     C
0  a  0  True
```

#### loc索引

```python
>>> af.set_index(index_cols='A')
>>> af
   A  B      C
A             
a  a  0   True
b  b  1   True
c  c  2  False
d  d  3  False
>>> af.loc['a','C']
True
>>> af.loc[list('bd'),list('AC')]
   A      C
A          
b  b   True
d  d  False
```

#### ix索引

类R语言data.frame的索引语法，使用pandas弃用的ix索引器。

```python
>>> af.ix[2,'B']
2
>>> af.ix[:2,list('AB')]
   A  B
A      
a  a  0
b  b  1
```
