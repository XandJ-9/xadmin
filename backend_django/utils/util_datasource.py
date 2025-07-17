import pymysql, psycopg2
from pyhive import hive, presto
from sshtunnel import SSHTunnelForwarder
import sys
from pathlib import Path

import environ,os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# environ.Env.read_env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

REMOTE_SERVER_IP = env('REMOTE_SERVER')  # 本地可访问的服务器地址
REMOTE_SERVER_PORT = env('REMOTE_SERVER_PORT')   # 本地可访问的远程端口
PRIVATE_SERVER_IP = env('PRIVATE_SERVER')  # 本地无法访问，但是中间服务器可访问
REMOTE_PASSWORD = env('REMOTE_PASSWORD')
REMOTE_USER = env('REMOTE_USER')

def remote_tunnel_server():
    if sys.platform == 'linux':
        return None

    # 创建隧道，登录到中间服务器上， 将local_bind_address指定的端口映射到远程的remote_bind_address指定的端口
    server = SSHTunnelForwarder((REMOTE_SERVER_IP, int(REMOTE_SERVER_PORT)),
        ssh_username=REMOTE_USER,
        ssh_password=REMOTE_PASSWORD,
        remote_bind_address=(PRIVATE_SERVER_IP, 10000),
        local_bind_address=('0.0.0.0', 10000)
        )
    return server


class BaseDataSourceHandler:
    pass

class DataSourceHandler(BaseDataSourceHandler):
    def __init__(self,db_info, *args, db_type=None, **kwargs):
        self.type = db_type
        self.db_info = db_info
        self.server = None
        self._connect = None


    def __new__(cls, *args, **kwargs):
        # return super().__new__()
        # return cls.init_handler(*args, **kwargs)
        ds_type = kwargs.pop('db_type', None)
        if ds_type == 'mysql':
            return MySqlDataSourceHandler(*args, **kwargs)
        elif ds_type == 'postgresql':
            return PostgreSqlDataSourceHandler(*args, **kwargs)
        elif ds_type == 'hive':
            return HiveDataSourceHandler(*args, **kwargs)
        return super().__new__(cls)

    def init_connection(self):
        raise NotImplementedError("Not Implemented")
    def __enter__(self):
        if sys.platform != 'linux':
            self.server = remote_tunnel_server()
            print('start tunnel....')
            self.server.start()
        self.init_connection()
        return self

    def __exit__(self, *args):
        if self.server:
            self.server.stop()



class DataSourceHandlerMix:
    def connection_test(self):
        if self._connect is None:
            self.init_connection()
        with self._connect.cursor() as cursor:
            cursor.execute("select 1")
        return True
    
    def table_list(self):
        if self._connect is None:
            self.init_connection()
        with self._connect.cursor() as cursor:
            cursor.execute("show tables")
            tables = [t[0] for t in cursor.fetchall()]
        return tables

class MySqlDataSourceHandler(DataSourceHandlerMix,DataSourceHandler):

    def init_connection(self):
        db_config = {
            'host':self.db_info.get('host',''),
            'port':self.db_info.get('port',3306),
            'user':self.db_info.get('user',''),
            'password':self.db_info.get('password',''),
            'database':self.db_info.get('database','')
        }
        self._connect = pymysql.connect(**db_config)
    
    def table_list(self, database=None):
        if database is None:
            database = self.db_info.get('database','')
        if self._connect is None:
            self.init_connection()
        tables = []
        with self._connect.cursor() as cursor:
            cursor.execute("SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_COMMENT,CREATE_TIME ,UPDATE_TIME  FROM information_schema.tables where TABLE_TYPE ='BASE TABLE' and TABLE_SCHEMA = %s", (database,))
            tables = [{
                "db_name":t[0],
                "table_name":t[1],
                "table_desc":t[2],
                "create_time":t[3].strftime('%Y-%m-%d %H:%M:%S'),
                "update_time":t[4].strftime('%Y-%m-%d %H:%M:%S') if t[4] else ''
            } for t in cursor.fetchall()]
        return tables

class PostgreSqlDataSourceHandler(DataSourceHandlerMix,DataSourceHandler):

    def init_connection(self):
        db_config = {
            'host':self.db_info.get('host',''),
            'port':self.db_info.get('port',3306),
            'user':self.db_info.get('user',''),
            'password':self.db_info.get('password',''),
            'database':self.db_info.get('database','')
        }
        self._connect = psycopg2.connect(**db_config)


class HiveDataSourceHandler(DataSourceHandlerMix,DataSourceHandler):


    def init_connection(self):
        db_config = {
            'host':self.db_info.get('host',''),
            'port':self.db_info.get('port',10000),
            'username':self.db_info.get('user',''),
            'password':self.db_info.get('password',''),
            'database':self.db_info.get('database','default')
        }
        try:
            print(db_config)
            self._connect = hive.Connection(**db_config, auth='CUSTOM')
        except:
            raise Exception('连接失败')

    def table_list(self, database=None):
        if database is None:
            database = self.db_info.get('database','default')
        if self._connect is None:
            self.init_connection()
        tables = []
        with self._connect.cursor() as cursor:
            cursor.execute("use %s" % database)
            cursor.execute("show tables")
            # cursor.execute("select current_date")
            tables = [{
                "db_name":t[0],
                "table_name":'',
                "table_desc":'',
                "create_time":'',
                "update_time":''
            } for t in cursor.fetchall()]
        return tables

if __name__=='__main__':
    # ds=DataSourceHandler({'type':'mysql','host': 'mysql-5632a4182a17-public.rds.volces.com', 'port': 3306, 'user': 'biadmin', 'password': 'vRt83wRYq7LV', 'database': 'newlink197'}, db_type='mysql')
    # with DataSourceHandler({'type':'hive','host': 'localhost', 'port': 10000, 'user': 'biadmin', 'password': '0S^tNOHRgNMw', 'database': 'ads'}, db_type='hive') as ds:
    with DataSourceHandler({'type':'hive','host': 'localhost', 'port': 10000, 'user': 'biadmin', 'password': '0S^tNOHRgNMw', 'database': 'ads'}, db_type='hive') as ds:
        # ds.init_connection()
        # print(ds._connect)
        tbList=ds.table_list()
        print(tbList)

