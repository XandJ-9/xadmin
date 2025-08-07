from typing import Dict, Any, Optional
import pymysql, datetime
from .base import QueryExecutor


# 自定义时间转换器：将 datetime 转为指定格式的字符串
def datetime_conv(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value

class MySQLQueryExecutor(QueryExecutor):
    def connect(self) -> pymysql.Connection:
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            conv={datetime: datetime_conv}
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

    def query_tables(self, database: str) -> Dict[str, Any]:
        connection = self.connect()
        cursor = connection.cursor()
        sql = 'SELECT * FROM information_schema.tables WHERE table_schema = %s'
        cursor.execute(sql, (database,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return {
            'list': result
        }
    
    def query_table_metadata(self, table_schema: str ,table_name: str) -> Dict[str, Any]:
        connection = self.connect()
        cursor = connection.cursor()
        # sql = 'SELECT * FROM information_schema.columns WHERE table_schema = %s AND table_name = %s'
        sql = '''
        SELECT 
            TABLE_CATALOG, 
            TABLE_SCHEMA, 
            TABLE_NAME, 
            COLUMN_NAME, 
            ORDINAL_POSITION, 
            COLUMN_DEFAULT, 
            IS_NULLABLE, 
            DATA_TYPE, 
            CHARACTER_MAXIMUM_LENGTH, 
            CHARACTER_OCTET_LENGTH, 
            NUMERIC_PRECISION, 
            NUMERIC_SCALE, 
            DATETIME_PRECISION, 
            CHARACTER_SET_NAME, 
            COLLATION_NAME, 
            COLUMN_TYPE, 
            COLUMN_KEY, 
            EXTRA, 
            `PRIVILEGES`, 
            COLUMN_COMMENT
        FROM information_schema.columns 
        WHERE table_schema = %s AND table_name = %s
        '''
        cursor.execute(sql, (table_schema, table_name))
        result = cursor.fetchall()
        return {
            'list': result
        }