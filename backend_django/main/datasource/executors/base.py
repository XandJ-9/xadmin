from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class QueryExecutor(ABC):
    def __init__(self, host: str = None, port: int = None, database: str = None, username: str = None, password: str = None):
        self.host = host 
        self.port = port 
        self.database = database 
        self.username = username
        self.password = password

    @abstractmethod
    def connect(self) -> Any:
        """建立数据库连接"""
        pass

    @abstractmethod
    def execute_query(self, sql: str, limit: Optional[int] = 10000) -> Dict[str, Any]:
        """执行SQL查询"""
        pass

    
    def execute_query_page(self, sql: str, page_num: int, page_size: int) -> Dict[str, Any]:
        """执行SQL查询并分页"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """测试数据库连接"""
        pass

    @abstractmethod
    def close(self) -> None:
        """关闭数据库连接"""
        pass


    def query_metadata(self, sql: str) -> Dict[str, Any]:
        """查询元数据"""
        pass
