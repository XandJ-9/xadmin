from typing import Dict, Any, Optional
from pyhive import presto, hive
from sshtunnel import SSHTunnelForwarder
from pathlib import Path
from .base import QueryExecutor


class PrestoQueryExecutor(QueryExecutor):
    # def connect(self) -> prestodb.Connection:
    #     return prestodb.dbapi.connect(
    #         host=self.host,
    #         port=self.port,
    #         user=self.username,
    #         catalog=self.database,
    #         schema=self.database
    #         )

    def connect(self)->presto.Connection:
        self.password = None
        if self.password:
            return presto.connect(host=self.host, port=self.port, user=self.username, password=self.password, protocol = 'https', schema=self.database)
        else:
            print(f'{self.username} {self.password} {self.host} {self.port} {self.database}')
            return presto.connect(host=self.host, port=self.port, username=self.username, password = self.password, schema=self.database)
        # return presto.connect(*self._args, **self._kwargs)
    def test_connection(self) -> bool:
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            connection.close()
            return True
        except Exception:
            return False

    def execute_query(self, sql: str, limit: Optional[int] = 10000) -> Dict[str, Any]:
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(sql)
            if sql.strip().lower().startswith('select'):
                results = cursor.fetchmany(limit)
                return {
                    'data': results,
                    'total': len(results)
                }
            else:
                connection.commit()
                return {
                    'message': '执行成功',
                    'affected_rows': cursor.rowcount
                }
        except Exception as e:
            raise Exception(f'执行失败: {e}')
        finally:
            if 'connection' in locals():
                connection.close()

    def execute_query_page(self, sql, page_num, page_size):
        return {}
    
    def close(self) -> None:
        # 由于每次查询都会创建新的连接，所以这里不需要实现
        pass


if __name__ == '__main__':
    import environ,os,sys
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    sys.path.append('.')
    env = environ.Env()
    # environ.Env.read_env()
    env_file = os.path.join(BASE_DIR, '.env')
    environ.Env.read_env(env_file)

    REMOTE_SERVER_IP = env('REMOTE_SERVER')  # 本地可访问的服务器地址
    REMOTE_SERVER_PORT = int(env('REMOTE_SERVER_PORT'))   # 本地可访问的远程端口
    PRIVATE_SERVER_IP = env('PRIVATE_SERVER')  # 本地无法访问，但是中间服务器可访问
    REMOTE_PASSWORD = env('REMOTE_PASSWORD')
    REMOTE_USER = env('REMOTE_USER')
    with SSHTunnelForwarder((REMOTE_SERVER_IP, REMOTE_SERVER_PORT),
    ssh_username=REMOTE_USER,
    ssh_password=REMOTE_PASSWORD,
    remote_bind_address=(PRIVATE_SERVER_IP, 8084),
    local_bind_address=('0.0.0.0', 8084)) as server:
        executor = PrestoQueryExecutor(
            host='localhost',
            port=8084,
            username='biadmin',
            ## password='0S^tNOHRgNMw',
            database='dwd'
        )
        res=executor.execute_query('select current_time')
    # executor = PrestoQueryExecutor(
    #     host='localhost',
    #     port=8084,
    #     database='default',
    #     username='root',
    #     password=None
    # )
    # res = executor.execute_query("select 100")
    print(res)
