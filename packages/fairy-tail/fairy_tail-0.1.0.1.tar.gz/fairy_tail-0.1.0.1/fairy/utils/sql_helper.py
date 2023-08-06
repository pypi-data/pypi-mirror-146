import time
import typing as t
from functools import wraps

import pymysql
from DBUtils.PooledDB import PooledDB


def db_wraps(func):
    @wraps(func)
    def __inner(ins, sql, args=None):
        conn, cursor = ins.create_conn()
        ret = func(ins, cursor, sql, args)
        ins.close_conn(conn, cursor)
        return ret

    return __inner


def retry(count=3):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            e = None
            for i in range(count):
                try:
                    ret = func(*args, **kwargs)
                    return ret
                except Exception as e:
                    time.sleep(0.1)
            raise e
        return inner
    return wrapper


class SQLHelper(object):

    def __init__(self, host, port, user, password, database, creator=pymysql, mincached=2, maxcached=5,
                 maxshared=1, maxconnections=6, blocking=True, maxusage=None, setsession=None, reset=True,
                 failures=None, ping=0, *args, **kwargs):
        '''
        :param host:
        :param port:
        :param user:
        :param password:
        :param database:
        :param creator: 使用链接数据库的模块
        :param mincached: 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        :param maxcached: 链接池中最多闲置的链接，0和None不限制
        :param maxshared: 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的
                            threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        :param maxconnections: 连接池允许的最大连接数，0和None表示不限制连接数
        :param blocking: 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        :param maxusage: 一个链接最多被重复使用的次数，None表示无限制
        :param setsession: 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        :param reset:
        :param failures:
        :param ping: ping MySQL服务端，检查是否服务可用。
            如：0 = None = never,
            1 = default = whenever it is requested,
            2 = when a cursor is created,
            4 = when a query is executed,
            7 = always
        :param args:
        :param kwargs:
        '''
        self.POOL = PooledDB(
            creator=creator,
            maxconnections=maxconnections,
            mincached=mincached,
            maxcached=maxcached,
            maxshared=maxshared,
            blocking=blocking,
            maxusage=maxusage,
            setsession=setsession,
            ping=ping,
            reset=reset,
            failures=failures,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8',
            *args, **kwargs
        )

    @retry()
    def create_conn(self):
        conn = self.POOL.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print('created...')
        return conn, cursor

    def close_conn(self, conn, cursor):
        cursor.close()
        conn.commit()
        conn.close()
        print('closed...')

    def _execute(self, sql, args=None):
        conn, cursor = self.create_conn()
        cursor.execute(sql, args)
        return conn, cursor

    @db_wraps
    def select(self, cursor, sql, args=None) -> t.List[t.Dict[str, t.Any]]:
        cursor.execute(sql, args)
        return cursor.fetchall()

    @db_wraps
    def select_one(self, cursor, sql, args=None) -> t.Dict[str, t.Any]:
        cursor.execute(sql, args)
        return cursor.fetchone()
    # def select(self, sql, args=None):
    #     conn, cursor = self._execute(sql, args)
    #     ret = QuerySet(cursor.fetchall())
    #     self.close_conn(conn, cursor)
    #     return ret

    # def select_one(self, sql, args):
    #     conn, cursor = self._execute(sql, args)
    #     ret = cursor.fetchone()
    #     self.close_conn(conn, cursor)
    #     return ret

    def select_all(self, sql, args=None):
        conn, cursor = self._execute(sql, args)
        ret = cursor.fetchall()
        self.close_conn(conn, cursor)
        return ret

    def insert(self, sql, args):
        conn, cursor = self._execute(sql, args)
        conn.commit()
        self.close_conn(conn, cursor)

    def update(self, sql, args):
        conn, cursor = self._execute(sql, args)
        conn.commit()
        self.close_conn(conn, cursor)
    #
    # def delete(self,sql, args):
    #     conn, cursor = self._execute(sql, args)
    #     conn.commit()
    #     self.close_conn(conn, cursor)


class QuerySet():
    def __init__(self, qs):
        # super().__init__(qs)
        self.__qs = qs

    def first(self):
        return self.__qs[0]

    def last(self):
        return self.__qs[-1]

    def all(self):
        return self.__qs

    def __str__(self):
        return f'{self.__class__}'


if __name__ == '__main__':
    db = SQLHelper(host='10.60.0.221', port=3306, user='root', password='123456', database='question')
    ret = db.select_one('select * from entity_subject limit 1')
    print(ret)