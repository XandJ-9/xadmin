from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from system.permissions import IsAdminUser, IsOwnerOrAdmin
from utils.viewset import CustomModelViewSet
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

    @action(detail=False, methods=['get'], url_path='types')
    def get_datasource_types(self, request):
        """
        获取所有数据源的简单信息
        """
        type_list = DataSource.objects.values_list('type')
        type_set = set(type_list)
        return Response(type_set)

    @action(detail=True, methods=['post'], url_path='test')
    def test_connection(self, request, pk=None):
        datasource = self.get_object()
        executor = QueryExecutorFactory.get_executor(datasource.type, host=datasource.host, port=datasource.port,database= datasource.database, username =datasource.username, password=datasource.password)
        try:
            if executor.test_connection():
                return Response({'status':'success','msg': '连接成功'}, status=status.HTTP_200_OK)
            return Response(
                {'status':'error','msg': '请检查数据源配置是否正确'},
                status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'status':'error','msg': '请检查数据源配置是否正确'},
                status=status.HTTP_200_OK
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
                status=status.HTTP_200_OK
            )
            

class QueryLogViewSet(CustomModelViewSet):
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
            queryset = QueryLog.objects.all()
            logger.info(f'{user.username}查询所有查询记录条数: {queryset.count()}')
        else:
            queryset = QueryLog.objects.filter(creator=user)
        return queryset