from typing import Dict, Any, Optional
import psycopg2
from psycopg2.extras import DictCursor
from .base import QueryExecutor

class PostgreSQLQueryExecutor(QueryExecutor):
    def connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.username,
            password=self.password
        )

    def test_connection(self) -> bool:
        try:
            connection = self.connect()
            connection.close()
            return True
        except Exception:
            return False

    def execute_query(self, sql: str, limit: Optional[int] = 10000) -> Dict[str, Any]:
        try:
            connection = self.connect()
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql)
                if sql.strip().lower().startswith('select'):
                    results = cursor.fetchmany(limit)
                    # 将结果转换为字典列表
                    results = [dict(row) for row in results]
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

    def close(self) -> None:
        # 由于每次查询都会创建新的连接，所以这里不需要实现
        pass