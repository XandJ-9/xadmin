from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from system.permissions import IsAdminUser, IsOwnerOrAdmin

from .models import DataSource, QueryLog
from .serializers import DataSourceSerializer, QueryLogSerializer
from .executors.factory import QueryExecutorFactory
import logging

logger = logging.getLogger('django')

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action == 'create':
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

        executor = QueryExecutorFactory.get_executor(datasource.type, 
        host=datasource.host, 
        port=datasource.port,
        database= datasource.database, 
        username =datasource.username, 
        password=datasource.password)

        try:
            result = executor.execute_query(sql, limit)
            return Response(result)
        except Exception as e:
            logger.error(f'SQL执行失败: {str(e)}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            

class QueryLogViewSet(viewsets.ModelViewSet):
    queryset = QueryLog.objects.all()
    serializer_class = QueryLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # filterset_fields = ['datasource_id', 'status', ]
    # search_fields = ['datasource_id', 'status', 'sta_date']

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or (user.role and user.role.name == 'admin'):
            return QueryLog.objects.all()
        return QueryLog.objects.filter(user=user)