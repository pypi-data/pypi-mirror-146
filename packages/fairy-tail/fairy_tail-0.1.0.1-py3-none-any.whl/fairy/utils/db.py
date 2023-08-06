'''
Author : hupeng
Time : 2021/12/21 14:50 
Description: 
'''
import time
import keyword
from functools import wraps, partial
from collections import abc
import logging
logging.basicConfig(level=logging.WARNING)

import pymysql
try:
    from DBUtils.PooledDB import PooledDB
except:
    # 2.0+版本
    from dbutils.pooled_db import PooledDB

import DBUtils
DBUtils.SteadyDB.SteadyDBCursor

cfg = {
    'host': '',
    'port': '',
    'user': '',
    'password': '',
    'database': ''
}
PoolDB = partial(PooledDB, creator=pymysql)

SHOW_TABLES = 'SHOW TABLES;'
SQL = {
    'create': 'insert into {table_name} ({columns}) values ({value})',
    'update': 'update {table_name} set {value} where id={id}',
    'delete': '',
    # 'select': '',
}


def db_wraps(func):
    @wraps(func)
    def __inner(ins, sql, args=None):
        conn, cursor = ins._get_connection()
        try:
            ret = func(ins, cursor, sql, args)
        except Exception as err:
            raise err
        finally:
            ins._recycle_connection(conn, cursor)
        return ret
    return __inner


class FrozenJson(object):

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(i) for i in arg]
        else:
            return arg

    def __init__(self, mapping):
        # print('__init__: ', mapping)
        self.__data = {}
        for k, v in mapping.items():
            if keyword.iskeyword(k):
                k += '_'
            self.__data[k] = v

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson(self.__data[name])

    def __getitem__(self, key):
        if isinstance(self.__data[key], (abc.MutableSequence, abc.Mapping)):
            return FrozenJson(self.__data[key])
        return self.__data[key]

    def __repr__(self):
        return str(self.__data)


sql = FrozenJson(SQL)


class DBHandler:
    __db = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        if 'charset' not in self._kwargs:
            self._kwargs['charset'] = 'utf8'

    def _get_connection(self):
        db_err = None
        try:
            if self.__db is None:
                self.__db = PoolDB(**self._kwargs)
            conn = self.__db.connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            return conn, cursor
        except Exception as e:
            self.__db = None
            max_retries = 0
            while not self.__db or max_retries <= 3:
                try:
                    self.__db = PoolDB(**self._kwargs)
                    conn = self.__db.connection()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    return conn, cursor
                except Exception as db_err:
                    time.sleep(0.1)
                    max_retries += 1
                    self._db = None
            raise db_err

    def _recycle_connection(self, conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            conn.commit()
            conn.close()

    def _recycle_connect_and_rollback(self, conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            conn.rollback()
            conn.close()

    def get_tables(self, db_name):
        conn, cursor = self._get_connection()
        try:
            cursor.execute(SHOW_TABLES)
            tables = cursor.fetchall()
            return [t[f'Tables_in_{db_name}'] for t in tables]
        finally:
            self._recycle_connection(conn, cursor)


class op:
    def __init__(self, name, db):
        self.name = name
        self.__db = db

    @db_wraps
    def execute(self, cursor, sql):
        logging.info(sql)
        cursor.execute(sql)
        return cursor

    def create(self, **kwargs):
        if not kwargs:
            raise ValueError('create params is empty!')
        conn, cursor = self.__db._get_connection()
        try:
            columns = tuple([str(i) for i in kwargs.keys()])
            values = tuple([str(i) for i in kwargs.values()])
            _sql = sql.create.format(
                table_name=self.name,
                columns=','.join(columns),
                value=','.join(values)
            )
            logging.info(_sql)
            cursor.execute(_sql)
            return cursor
        except Exception as err:
            raise err
        finally:
            self.__db._recycle_connection(conn, cursor)

    def update(self, primary_id, **kwargs):
        pass

    def delete(self, primary_id):
        pass

    def select(self):
        pass

    def __str__(self):
        conn, cursor = self.__db._get_connection()
        cursor.execute(f'DESCRIBE {self.name}')
        desc = cursor.fetchall()
        head = ''
        for field in desc:
            head += '\t'.join([f'{k}: {v}' for k, v in field.items()]) + '\n'
        return head

from threading import Lock
lock = Lock()
class DB(DBHandler):
    def __init__(self, **kwargs):
        database = kwargs['database']
        super().__init__(**kwargs)
        self.__tables = {}
        for t in self.get_tables(database):
            if keyword.iskeyword(t):
                t += '_'
            self.__tables[t] = op(t, self)
        self.__dict__.update(self.__tables)

    @property
    def tables(self):
        return self.__tables

    @db_wraps
    def execute(self, cursor, sql):
        logging.info(sql)
        cursor.execute(sql)
        # res = cursor.fetchall()
        # return FrozenJson(res)
        return cursor

    def __enter__(self):
        lock.acquire()
        self.conn, self.cursor = self._get_connection()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self._recycle_connection(self.conn, self.cursor)
        else:
            self._recycle_connect_and_rollback(self.conn, self.cursor)
        del self.conn, self.cursor
        lock.release()

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return str(self.__tables)


class DBManager(object):
    def __init__(self, cfg):
        self.__databases = {}
        if isinstance(cfg, abc.Mapping):
            _db = cfg['database']
            self.__databases[_db] = DB(**cfg)
        elif isinstance(cfg, abc.MutableSequence):
            for item in cfg:
                _db = item['database']
                self.__databases[_db] = DB(**item)

    def __getattr__(self, name):
        if hasattr(self.__databases, name):
            return getattr(self.__databases, name)
        else:
            return self.__databases[name]

    def init(self):
        pass

    def __repr__(self):
        return str(self.__databases)


if __name__ == '__main__':
    cfg = [
        {
            'host': '10.60.0.221',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'question'
        },
        {
            'host': '10.60.0.221',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'poem'
        }
    ]
    db = DBManager(cfg)
    # print(db)
    # print(db.question)
    # print(db.poem)
    # print(db.question.tables)
    # res = db.question.id2question_id.create(question_id=1434)
    # print(res._cursor)
    # print(res.lastrowid)
    print(db.question.id2question_id)
    # s = db.question.execute('select * from entity_subject where id=1').fetchall()
    # print(s)
    # print(s[0].name)
    with db.question as cursor:
        pass
        # res = d.execute('select * from entity_grade')
        # print(res)
