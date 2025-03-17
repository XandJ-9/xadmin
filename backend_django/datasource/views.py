from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DataSource
from .serializers import DataSourceSerializer
from users.permissions import IsAdminUser, IsOwnerOrAdmin
from .executors.factory import QueryExecutorFactory
import logging

logger = logging.getLogger('django')

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (user.role and user.role.name == 'admin'):
            return DataSource.objects.all()
        return DataSource.objects.filter(creator=user)

    @action(detail=True, methods=['post'], url_path='test')
    def test_connection(self, request, pk=None):
        datasource = self.get_object()
        executor = QueryExecutorFactory.get_executor(datasource.type, host=datasource.host, port=datasource.port,database= datasource.database, username =datasource.username, password=datasource.password)
        try:
            if executor.test_connection():
                return Response({'message': '连接成功'}, status=status.HTTP_200_OK)
            return Response(
                {'error': '连接失败'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f'数据源连接测试失败: {str(e)}')
            return Response(
                {'error': f'连接失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], url_path='query')
    def execute_query(self, request, pk=None):
        datasource = self.get_object()
        sql = request.data.get('sql')
        limit = request.data.get('limit', 10000)

        if not sql:
            return Response(
                {'error': 'SQL语句不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        executor = QueryExecutorFactory.get_executor(datasource.type, host=datasource.host, port=datasource.port,database= datasource.database, username =datasource.username, password=datasource.password)

        try:
            result = executor.execute_query(sql, limit)
            return Response(result)
        except Exception as e:
            logger.error(f'SQL执行失败: {str(e)}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )