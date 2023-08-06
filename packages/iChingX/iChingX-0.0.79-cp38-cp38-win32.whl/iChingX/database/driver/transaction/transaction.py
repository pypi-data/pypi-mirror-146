#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：iChingX 
@File    ：transaction.py
@IDE     ：PyCharm 
@Author  ：Alex
@Date    ：2022/4/12 20:04
事务处理with包装处理类
'''
class Transaction():

    def query(self, sql: str, bind:(list,tuple,dict)=None, master: bool = False) -> list:
        '''
        query方法用于执行SQL查询操作，返回查询结果数据集（数组）。
        :param str sql:                     SQL语句
        :param list|tuple|dict bind:        参数绑写
        :param bool master:                 是否使用主库查询
        :return: list
        '''
        pass

    def execute(self, sql: str, bind:(list,tuple,dict)=None) -> (bool, int):
        '''
        execute用于更新和写入数据的sql操作，如果数据非法或者查询错误则返回false，否则返回影响的记录数。
        :param str sql:                     SQL语句
        :param list|tuple|dict bind:        参数绑定
        :return:    bool|int
        '''
        pass
