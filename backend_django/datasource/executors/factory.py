from typing import Dict, Type
from .base import QueryExecutor
from .mysql import MySQLQueryExecutor
from .postgresql import PostgreSQLQueryExecutor
from .starrocks import StarRocksQueryExecutor

class QueryExecutorFactory:
    _executors: Dict[str, Type[QueryExecutor]] = {
        'mysql': MySQLQueryExecutor,
        'postgresql': PostgreSQLQueryExecutor,
        'starrocks': StarRocksQueryExecutor
    }

    @classmethod
    def get_executor(cls, datasource_type: str, **kwargs) -> QueryExecutor:
        """根据数据源类型获取对应的查询执行器实例

        Args:
            datasource_type: 数据源类型
            **kwargs: 数据源连接参数

        Returns:
            QueryExecutor: 查询执行器实例

        Raises:
            ValueError: 当数据源类型不支持时抛出异常
        """
        executor_class = cls._executors.get(datasource_type.lower())
        if not executor_class:
            raise ValueError(f'不支持的数据源类型: {datasource_type}')
        return executor_class(**kwargs)

    @classmethod
    def register_executor(cls, datasource_type: str, executor_class: Type[QueryExecutor]) -> None:
        """注册新的查询执行器

        Args:
            datasource_type: 数据源类型
            executor_class: 查询执行器类
        """
        cls._executors[datasource_type.lower()] = executor_class