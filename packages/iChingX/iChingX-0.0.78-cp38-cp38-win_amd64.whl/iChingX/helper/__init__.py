#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：iChingCore 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：Alex
@Date    ：2022/3/22 18:26 
'''
from ._env import __EnvInstance
Env = __EnvInstance()

from ._utils import Utils
from ._str import Str
from ._arr import Arr
from ._json import Json
from ._hash import Hash
from ._date import Date
from ._human import Human
from ._log import Log
from ._config import Config

from ._cache import __CacheManager
Cache = __CacheManager()

from iChingX.database.db_manager import DBManager
Db = DBManager()

