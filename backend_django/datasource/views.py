from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
            
    @action(detail=False, methods=['get'], url_path='query-logs')
    def query_logs(self, request):
        user = request.user
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        datasource_id = request.query_params.get('datasource_id')
        status_filter = request.query_params.get('status')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # 根据用户角色过滤查询日志
        if user.is_superuser or (user.role and user.role.name == 'admin'):
            queryset = QueryLog.objects.all()
        else:
            queryset = QueryLog.objects.filter(user=user)
        
        # 应用过滤条件
        if datasource_id:
            queryset = queryset.filter(datasource_id=datasource_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            
        # 计算分页
        total = queryset.count()
        start = (page - 1) * page_size
        end = page * page_size
        queryset = queryset[start:end]
        
        serializer = QueryLogSerializer(queryset, many=True)
        
        return Response({
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })