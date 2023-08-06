# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 23:10:03 2021

@author: yonder_sky
"""

# arraytool生成文件，春秋迭代，yondersky@126.com，2021-10-13
# 更新日期：2022-03-12

import setuptools

with open('README.md','r',encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = 'arraytool',
    version = '0.1.4',
    author = '春秋迭代',
    author_email = 'yondersky@126.com',
    description = '基于numpy的Series及DataFrame数据结构',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://gitee.com/yonder_sky/arraytool',
    packages = setuptools.find_packages(),
    # install_requires = ['orderedset'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
