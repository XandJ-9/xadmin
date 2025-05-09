from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class QueryExecutor(ABC):
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
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

    @abstractmethod
    def test_connection(self) -> bool:
        """测试数据库连接"""
        pass

    @abstractmethod
    def close(self) -> None:
        """关闭数据库连接"""
        pass