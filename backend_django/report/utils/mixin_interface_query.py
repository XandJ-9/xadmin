import traceback
from django.http.response import HttpResponseNotFound, JsonResponse
from django.template import Template, Context
from rest_framework.decorators import action
from ..models  import InterfaceInfo,InterfaceField,InterfaceQueryLog

from .operation_interface_query import InterfaceQueryResult
from utils.util_datetime import getNowTimestamp
import logging


logger = logging.getLogger(__name__)

class InterfaceQueryMixin:

    @action(detail=False, methods=['post'])
    def query_interface(self, request):
        '''
        获取接口信息：
        1. 数据源
        2. 接口查询语句
        3， 包装返回结构
        '''
        interface_code = request.query_params.get("interface_code")
        interface_info = InterfaceInfo.objects.filter(interface_code=interface_code).first()
        query_params = request.data
        if not interface_info:
            return HttpResponseNotFound(content="接口不存在")
        try:
            # 解析查询sql，并执行查询
            interface_sql_template = Template(interface_info.interface_sql)
            interface_sql = interface_sql_template.render(Context(query_params))
        except Exception as e:
            return JsonResponse({
                "code": "-1",
                "message": str(e)
            })
        
        if interface_info.is_total == "1":
            total_sql_template = Template(interface_info.total_sql)
            total_sql = total_sql_template.render(Context(query_params))
        else:
            total_sql = None
        # 获取数据源
        execute_start_time = getNowTimestamp()
        execute_result = ''
        error_message = None
        query_obj = InterfaceQueryResult(interface_info)  # 初始化查询结果对象

        try:
            query_obj.execute_query(interface_sql=interface_sql,total_sql=total_sql, offset = query_params.get('page_no', 1), limit=query_params.get('page_size', 10000))
            execute_result = "success"
        except Exception as e:
            logger.error(traceback.format_exc())
            error_message = str(e)
            execute_result = "error"
        finally:
            execute_end_time = getNowTimestamp()
            execute_time = execute_end_time - execute_start_time
            # 记录查询日志
            interface_query_log = InterfaceQueryLog.objects.create(interface_code=interface_code,
                                            interface_sql=interface_sql,
                                            query_params=query_params,
                                            execute_time=execute_time,
                                            execute_start_time=execute_start_time,
                                            execute_end_time=execute_end_time,
                                            execute_result=execute_result,
                                            error_message=error_message,
                                            creator = request.user if request.user.is_authenticated else None)
            interface_query_log.save()
        return JsonResponse(query_obj.get_result())
    


