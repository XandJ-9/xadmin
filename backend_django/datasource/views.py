from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DataSource
from .serializers import DataSourceSerializer
from users.permissions import IsAdminUser, IsOwnerOrAdmin
import pymysql
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

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        datasource = self.get_object()
        try:
            connection = pymysql.connect(
                host=datasource.host,
                port=datasource.port,
                user=datasource.username,
                password=datasource.password,
                database=datasource.database
            )
            connection.close()
            return Response({'message': '连接成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'数据源连接测试失败: {str(e)}')
            return Response(
                {'error': f'连接失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def execute_query(self, request, pk=None):
        datasource = self.get_object()
        sql = request.data.get('sql')

        if not sql:
            return Response(
                {'error': 'SQL语句不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            connection = pymysql.connect(
                host=datasource.host,
                port=datasource.port,
                user=datasource.username,
                password=datasource.password,
                database=datasource.database,
                cursorclass=pymysql.cursors.DictCursor
            )

            with connection.cursor() as cursor:
                cursor.execute(sql)
                if sql.strip().lower().startswith('select'):
                    results = cursor.fetchall()
                    return Response({
                        'data': results,
                        'total': len(results)
                    })
                else:
                    connection.commit()
                    return Response({
                        'message': '执行成功',
                        'affected_rows': cursor.rowcount
                    })

        except Exception as e:
            logger.error(f'SQL执行失败: {str(e)}')
            return Response(
                {'error': f'执行失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        finally:
            if 'connection' in locals():
                connection.close()