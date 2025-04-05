from django.utils.deprecation import MiddlewareMixin
import time
import logging
from .models import QueryLog

logger = logging.getLogger('django')

class QueryLogMiddleware(MiddlewareMixin):
    """中间件，用于记录SQL查询日志"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    # def __call__(self, request):
    #     # 处理请求前的代码
    #     response = self.get_response(request)

    #     # 处理请求后的代码
    #     return self.process_response(request, response)


    def process_view(self, request, view_func, view_args, view_kwargs):
        # 只处理数据源查询API
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return None
            
        # 只处理数据查询请求
        if request.resolver_match.url_name != 'datasource-execute-query':
            return None
        

        # 设置开始时间
        request.query_start_time = time.time()
        logger.info(f'开始记录查询日志: {request.query_start_time}')
        return None
        
    def process_response(self, request, response):
        # 处理查询日志记录
        if not hasattr(request, 'query_start_time'):
            return response

        # 计算执行时间
        execution_time = time.time() - request.query_start_time

        # 获取请求和响应数据
        try:
            if request.user.is_anonymous:
                return response
            
            # 获取数据源ID
            datasource_id = request.resolver_match.kwargs.get('pk')
            if not datasource_id:
                return response

            # 解析请求数据 
            # 将httprequest转换为rest_framework.request.Request对象
            from rest_framework.request import Request
            from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
            new_request = Request(request, parsers=[JSONParser(), FormParser(), MultiPartParser()])
            

            # 获取SQL和结果
            sql = new_request.data.get('sql', '')
            # sql = request.POST.get('sql') if request.method == 'POST' else request.GET.get('sql')
            logger.info(f'记录查询SQL: {sql}')

            if not sql:
                return response
                
            # 判断查询状态
            status_code = 'success'
            error_message = None
            result_count = 0
            
            # 检查响应状态
            if hasattr(response, 'data'):
                if 'error' in response.data:
                    status_code = 'error'
                    error_message = response.data.get('error')
                elif isinstance(response.data, list):
                    result_count = len(response.data)
                elif isinstance(response.data, dict) and 'data' in response.data:
                    result_count = len(response.data.get('data', []))
            
            # 创建查询日志
            QueryLog.objects.create(
                datasource_id=datasource_id,
                user=request.user,
                sql=sql,
                status=status_code,
                error_message=error_message,
                execution_time=execution_time,
                result_count=result_count
            )
            
        except Exception as e:
            logger.error(f'记录查询日志失败: {str(e)}')
            
        return response