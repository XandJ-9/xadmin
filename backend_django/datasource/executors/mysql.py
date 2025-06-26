from typing import Dict, Any, Optional
import pymysql
from .base import QueryExecutor

class MySQLQueryExecutor(QueryExecutor):
    def connect(self) -> pymysql.Connection:
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def test_connection(self) -> bool:
        try:
            connection = self.connect()
            try:
                connection.close()
                return True
            except:
                return False
        except Exception as e:
            raise e
            # return False

    def execute_query(self, sql: str, limit: Optional[int] = 10000) -> Dict[str, Any]:
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
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
            raise Exception(f'执行失败: {str(e)}')
        finally:
            if 'connection' in locals():
                connection.close()

    def execute_query_page(self, sql: str, page_num: int, page_size: int) -> Dict[str, Any]:
        offset = (page_num - 1) * page_size
        paginated_sql = f"{sql} LIMIT {offset}, {page_size}"
        return self.execute_query(paginated_sql)
    def close(self) -> None:
        # 由于每次查询都会创建新的连接，所以这里不需要实现
        pass