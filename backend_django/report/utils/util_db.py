from django.db import connections
import mysql.connector 


class DbException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg


class SqlHandler():
    pass

class MySqlHandler(SqlHandler):
    def __init__(self, dbname):
        self.dbname = dbname

    def query(self, sql:str, *args, **kwargs):
        with connections[self.dbname].cursor() as cursor:
            try:
                cursor.execute(sql, *args, **kwargs)
                columns = [c[0] for c in cursor.description]
                # print(columns)
                for item in cursor.fetchall():
                    item = dict(zip(columns, item))
                    yield item
                    # print(item)
            except:
                raise DbException('执行sql出错')
    
    def truncate(self, table:str):
        sql = f'truncate table {table}'
        with connections[self.dbname].cursor() as cursor:
            try:
                cursor.execute(sql)
            except Exception as e:
                cursor.connection.rollback()
                raise DbException('执行sql出错',e)
                

class HiveSqlHandler(SqlHandler):
    pass

class SparkSqlHandler(SqlHandler):
    pass

class PrestSqlHandler(SqlHandler):
    pass

class PostgreSqlHandler(SqlHandler):
    pass


#  数据源查询连接对象
class QueryConnection(object):
    pass

class MySqlConnection(QueryConnection):
    def __init__(self, *args, **kwargs) -> None:
        self.connection = mysql.connector.connect(*args, **kwargs)

class PostgreSqlConnection(QueryConnection):
    pass

class HiveConnection(QueryConnection):
    pass

class SparkConnection(QueryConnection):
    pass

class MySqlConnectionWrapper:
    '''
        'NAME': 'etlctl',
        'USER': 'biuser',
        'PASSWORD': 'biuser123',
        'HOST': 'gz-cdb-4pl2iqyv.sql.tencentcdb.com',
        'PORT': '60126',
    '''
    def __init__(self, db_info):
        self.parmas = {
            'host' : db_info['db_server'] # 连接名称，默认127.0.0.1
            ,'user' : db_info['db_user'] # 用户名
            ,'passwd':db_info['db_pwd'] # 密码
            ,'port': db_info['db_port'] # 端口，默认为3306
            ,'db':db_info['db_name'] # 数据库名称
            ,'charset':'utf8' # 字符编码
        }
        
    def get_connection(self):
        return MySqlConnection(**self.parmas)

def get_query_connection(db_info):
    db_type = db_info.get('db_type')
    if db_type == 'mysql':
        return MySqlConnectionWrapper(db_info).get_connection()
    elif db_type == 'postgresql':
        return PostgreSqlConnection
    # elif db_type == 'hive':
    #     return HiveSqlHandler
    # elif db_type == 'spark':
    #     return SparkSqlHandler
    # elif db_type == 'presto':
    #     return PrestSqlHandler
    else:
       raise DbException('不支持的数据库类型')
    

