#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：iChingCore 
@File    ：raw.py
@IDE     ：PyCharm 
@Author  ：Alex
@Date    ：2022/4/10 0:05
SQL Raw
'''
class Raw():

    # 查询表达式
    __value: str = ''

    # 参数绑定
    __bind = None

    def __init__(self,value:str,bind= None):
        '''
        创建一个查询表达式
        :param str value:
        :param list|tuple|dict bind:
        '''
        pass

    def getValue(self) -> str:
        '''
        获取表达式
        :return:
        '''
        pass

    def getBind(self) -> dict:
        '''
        获取参数绑定
        :return:
        '''
        pass