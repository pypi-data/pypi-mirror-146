#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：iChingCore 
@File    ：base_driver.py
@IDE     ：PyCharm 
@Author  ：Alex
@Date    ：2022/4/8 19:55
SQL关系型数据库驱动基类
'''
from iChingX.database.query.base_query import BaseQuery

class BaseDriver():

    @property
    def dbType(self) -> str:
        '''
        返回数据库类型
        :return str:
        '''
        pass

    def getConfig(self,key:(str,None) = None,default = None):
        '''
        获取数据库的配置参数
        :param str|None key:
        :param default:
        :return:
        '''
        pass

    def close(self):
        '''
        关闭连接
        :return:
        '''
        pass

    def newQuery(self) -> BaseQuery:
        '''
        创建查询对象
        :return: BaseQuery
        '''
        pass

    def table(self,table:(str,list,tuple,set,dict)) -> BaseQuery:
        '''
        指定表名开始查询
        :param str|list|tuple|set|dict table:
        :return: BaseQuery
        '''
        pass

    def name(self,name:(str,list,tuple,set,dict)) -> BaseQuery:
        '''
        指定表名开始查询(不带前缀)
        :param str|list|tuple|set|dict name:
        :return: BaseQuery
        '''
        pass

    def value(self,query:(BaseQuery,str),field:str,default = None):
        '''
        得到某个字段的值
        :param BaseQuery|str query:     BaseQuery查询对象或sql字符串
        :param str field:               字段名
        :param mixed default:           设置默认值，默认为None
        :return: mixed
        '''
        pass

    def column(self, query:(BaseQuery,str), column:str, key: str = '') -> list:
        '''
        得到某个列的数组
        :param BaseQuery|str query:     BaseQuery查询对象或sql字符串
        :param str column:              字段名
        :param str key:                 索引
        :return: list
        '''
        pass


    def query(self,sql:str,bind:(list,tuple,dict,None)=None,master:bool= False) -> list:
        '''
        query方法用于执行SQL查询操作，返回查询结果数据集（数组）。
        :param str sql:                     SQL语句
        :param list|tuple|dict|None bind:        参数绑定
        :param bool master:                 是否使用主库查询
        :return: list
        '''
        pass

    def execute(self,sql:str,bind:(list,tuple,dict,None) = None) -> (bool,int):
        '''
        execute用于更新和写入数据的sql操作，如果数据非法或者查询错误则返回false，否则返回影响的记录数。
        :param str sql:                     SQL语句
        :param list|tuple|dict bind:        参数绑定
        :return:    bool|int
        '''
        pass

    def statement(self,sql:str,bind:(list,tuple,dict,None)=None):
        '''
        statement方法用来运行不会有任何返回值的数据库语句。
        :param str sql:                 SQL语句
        :param list|tuple|dict bind:    参数绑定
        :return: void
        '''
        pass

    def fetchone(self,sql:str,bind:(list,tuple,dict,None)=None,master:bool= False) -> (dict,None):
        '''
        返回第一行数据
        :param str sql:                     SQL语句
        :param list|tuple|dict|None bind:        参数绑定
        :param bool master:                 是否使用主库查询，默认False
        :return: dict | None
        '''
        pass

    def fetchall(self,sql:str,bind:(list,tuple,dict,None)=None,master:bool= False) -> list:
        '''
        获取所有行数据源
        :param str sql:                     SQL语句
        :param list|tuple|dict|None bind:        参数绑定
        :param bool master:                 是否使用主库查询
        :return: list
        '''
        pass

    def prepareSQL(self,sql:str,bind:(list,tuple,dict,None)= None):
        '''
        预编译SQL语句
        :param str sql:
        :param list|tuple|dict|dict bind:
        :return:
        '''
        pass

    def getLastSql(self) -> str:
        '''
        获取最近一次查询的sql语句
        :return:
        '''
        pass

    def getLastError(self) -> Exception:
        '''
        返回最后的错误信息
        :return: Exception
        '''
        pass

    def getRealSql(self,sql:str,bind:(list,tuple,dict,None) = None) -> str:
        '''
        根据参数绑定组装最终的SQL语句 便于调试
        :param str sql:                 sql语句
        :param list|tuple|dict|None bind:    参数绑定列表
        :return: str
        '''
        pass

    def escape_string(self,value:str) ->str:
        '''
        字符串过滤，防止SQL注入
        :param str value:
        :return: str
        '''
        pass
