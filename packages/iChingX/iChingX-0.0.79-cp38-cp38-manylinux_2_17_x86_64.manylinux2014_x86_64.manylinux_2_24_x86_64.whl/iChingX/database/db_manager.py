#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：iChingCore
@File    ：db_manager.py
@IDE     ：PyCharm
@Author  ：Alex
@Date    ：2022/4/7 23:25
数据库管理包
'''
from iChingX.database.driver.base_driver import BaseDriver
from iChingX.database.query.base_query import BaseQuery
from iChingX.database.query.raw import Raw
from iChingX.database.constants import DRIVER_TYPES
from iChingX.database.driver.transaction.transaction import Transaction
from iChingX.database.driver.transaction.transaction_xa import TransactionXa

class DBManager():

    DRIVER_TYPE_MYSQL,DRIVER_TYPE_SQLITE,DRIVER_TYPE_REDIS,DRIVER_TYPE_MONGO = DRIVER_TYPES

    @property
    def dbType(self) -> str:
        '''
        返回数据库类型
        :return str:
        '''
        pass

    def getVersion(self)->str:
        '''
        查看数据库版本
        :return: str
        '''
        pass

    def getDatabases(self,exclude:bool = True) -> list:
        '''
        获取所有数据库信息
        :param bool exclude:        是否过滤系统数据库
        :return:
        '''
        pass

    def getDbUsage(self,
                   dbName:(bool,str,list,tuple,None) = None,
                   unit:(str,bool)= True)->(dict,list,None):
        '''
        获取数据库使用容量大小
        :param bool|str|list|tuple|None dbName:      数据库名称，str|list|tuple查询指定数据库，bool查询所有数据库，None=False
        :param str|bool unit:                   显示单位，可选值：KB，MB，GB，True（自动）,False不转换
        :return: dict|list|None
            {
                database:数据库名,
                tables:数据表数量,
                records:表记录数量,
                data_usage:数据容量
                index_usage:索引容量
                free_usage:碎片占用容量
            }
        '''
        pass

    def getTables(self,
                  dbName:(str,list,tuple,set,bool,None)=None,
                  prefix:(bool,None)=None,
                  exclude:bool = True) -> (list,None):
        '''
        获取数据库所有表名
        :param str|list|tuple|set|bool|None dbName: 指定数据库名称，None获取当前配置中的数据库，True获取所有数据库表，str指定数据库
        :param bool|None prefix: 是否添加数据库前缀，None自动，True添加，False不添加
        :param bool exclude: 是否过滤系统数据表,默认值：True
        :return: list|None
        '''
        pass

    def getTablesUsage(self,
                       tableName:(str,list,tuple,set,None) = None,
                       dbName:(str,None) = None,
                       unit:(str,bool) = True,
                       exclude:bool = True)->(list,dict,None):
        '''
        查看表容量大小，多表时只能查询同一数据库
        :param str|list|tuple|set|None tableName:   指定查询的表名
        :param str|None dbName:                     指定数据库名称，None获取当前配置中的数据库，str指定数据库名称
        :param str|bool unit:                       显示单位，可选值：KB，MB，GB，True（自动）,False不转换
        :param bool exclude: 是否过滤系统数据表,默认值：True
        :return: list|None
        :return: list|dict|None
            {
                database:数据库名,
                table:表名,
                records:表记录数量,
                data_usage:数据容量
                index_usage:索引容量
                free_usage:碎片占用容量
            }
        '''
        pass

    def getFields(self,tableName:str,force:bool = False) -> dict:
        '''
        获取数据表原生字段信息，读取后缓存记录
        :param str tableName:       表名
        :param bool force:          是否强制读取
        :return: dict
        '''
        pass

    def getSchemaInfo(self,tableName:str,force:bool = False) -> dict:
        '''
        获取表结构信息
        :param str tableName:       表名
        :param bool force:          是否强制读取，默认值False
        :return: dict
        '''
        pass

    def getPk(self,tableName:str) -> (str,list):
        '''
        获取数据表的主键
        :param str tableName:       表名
        :return: str|list
        '''
        pass

    def getAutoInc(self,tableName:str) -> str:
        '''
        获取数据表的自增长字段
        :param str tableName:
        :return: str
        '''
        pass

    def getFieldsDefaultVal(self,tableName:str,field:(str,list,tuple,set,None) = None):
        '''
        获取字段的默认值
        :param str tableName:                   表名
        :param str|list|tuple|set:None field:        指定获取的字段，默认值None时查询全部字段
        :return:
        '''
        pass

    def connect(self, name: str = None, force: bool = False) -> BaseDriver:
        '''
        创建/切换数据库连接查询
        :param str name:    连接配置标识
        :param bool force:  强制重新连接，默认False
        :return: BaseQuery
        '''
        pass

    def close(self,name:str = None):
        '''
        关闭连接
        :param str name:    连接名
        :return void:
        '''
        pass

    def table(self,table) -> BaseQuery:
        '''
        指定表名开始查询
        :param str|list|set|tuple|dict table:       表名
        :return:    BaseQuery
        '''
        pass

    def name(self,name) -> BaseQuery:
        '''
        指定表名开始查询(不带前缀)
        :param str|list|set|tuple|dict name:  表名，不带前缀
        :return:
        '''
        pass

    def Raw(self,value:str,bind = None) -> Raw:
        '''
        返回Raw对象
        :param str value:                   sql语句
        :param list|tuple|dict bind:        查询参数
        :return: Raw
        '''
        pass

    def query(self,sql:str,bind:(list,tuple,dict) = None,master:bool= False) -> list:
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

    def statement(self,sql:str,bind:(list,tuple,dict)=None):
        '''
        statement方法用来运行不会有任何返回值的数据库语句。
        :param str sql:                 SQL语句
        :param list|tuple|dict bind:    参数绑定
        :return: void
        '''
        pass

    def getLastSql(self) -> str:
        '''
        获取最近一次查询的sql语句
        :return:
        '''
        pass

    def getRealSql(self,sql,bind:(list,tuple,dict) = None) -> str:
        '''
        根据参数绑定组装最终的SQL语句 便于调试
        :param str sql:                 sql语句
        :param list|tuple|dict bind:    参数绑定列表
        :return: str
        '''
        pass

    def transaction(self, name:(str,BaseDriver) = None, force: bool = False) -> Transaction:
        '''
        执行数据库事务 with闭包方法
        :param str|BaseDriver name:         数据库连接实例或连接名
        :param bool force:           是否强制重新连接，默认值False
        :return: Transaction
        '''
        pass

    def transactionXa(self,connects:(str,BaseDriver,list,tuple,set) = None,force:bool = False) -> TransactionXa:
        '''
        执行数据库Xa事务 - 实现全局分布式事务
        :param str|list|tuple|set connects:
        :param bool force:      是否强制重新连接，默认值False
        :return: TransactionXa
        '''
        pass

    def startTrans(self):
        '''
        启动事务
        :return:
        '''
        pass

    def commit(self):
        '''
        提交事务
        :return:
        '''
        pass

    def rollback(self):
        '''
        回滚事务
        :return:
        '''
        pass



