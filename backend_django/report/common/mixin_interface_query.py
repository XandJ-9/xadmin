import traceback
from django.http.response import HttpResponseNotFound, JsonResponse
from django.template import Template, Context
from rest_framework.decorators import action
from ..models  import InterfaceInfo,InterfaceField,InterfaceQueryLog

from .operation_interface_query import wrap_query_result
from datasource.models import DataSource
from datasource.executors.factory import QueryExecutorFactory
import time,logging


logger = logging.getLogger(__name__)

class InterfaceQueryMixin:

    @action(detail=False, methods=['POST'], url_path='execute-query')
    def query_interface(self, request, interface_code=None):
        '''
        获取接口信息：
        1. 数据源
        2. 接口查询语句
        3， 包装返回结构
        '''
        interface_code = request.query_params.get("interface_code")
        interface_info = InterfaceInfo.objects.filter(interface_code=interface_code).first()
        if not interface_info:
            return HttpResponseNotFound(content="接口不存在")
        interface_db_type = interface_info.interface_db_type
        interface_db_name = interface_info.interface_db_name
        interface_fields = InterfaceField.objects.filter(interface=interface_info)
        # 获取数据源
        execute_start_time = time.time()
        executor = self.get_executor(interface_db_type, interface_db_name)
        # 解析查询sql，并执行查询
        interface_sql_template = Template(interface_info.interface_sql)
        interface_sql = interface_sql_template.render(Context(request.data))
        execute_end_time = time.time()
        execute_time = execute_end_time - execute_start_time
        query_result = executor.execute_query(interface_sql)
        # 结果包装
        result = wrap_query_result(query_result, interface_fields, interface_info)
        # 记录查询日志
        try:
            interface_query_log = InterfaceQueryLog.objects.create(interface_code=interface_code,
                                            interface_sql=interface_sql,
                                            execute_time=execute_time,
                                            execute_start_time=execute_start_time,
                                            execute_end_time=execute_end_time,
                                            execute_result="success",
                                            creator = request.user)
            interface_query_log.save()
        except:
            logger.error(traceback.format_exc())
        return JsonResponse(result)
    
    def get_executor(self, interface_db_type, interface_db_name):
        datasource = DataSource.objects.filter(type=interface_db_type,database=interface_db_name).first()
        executor =QueryExecutorFactory.get_executor(datasource_type=datasource.type,
                                            host=datasource.host, 
                                            port=datasource.port,
                                            database= datasource.database, 
                                            username =datasource.username, 
                                            password=datasource.password)
        return executor

