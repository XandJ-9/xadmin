# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from urllib.parse import quote
from django.http import HttpResponse
from rest_framework.response import Response

class SuccessResponse(Response):
    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None,page=1,limit=1,total=1):
        std_data = {
                "page": page,
                "limit": limit,
                "total": total,
                "data": data
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class DetailResponse(Response):
    """
    不包含分页信息的接口返回,主要用于单条数据查询
    (1)默认code返回2000, 不支持指定其他返回码
    """

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None,):
        std_data = {
            "msg": msg
        }
        
        if data:
            std_data['data'] = data
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回400, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(self, data=None, msg='error', code=None, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)

<<<<<<< HEAD
=======
class ExcelResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        filename = kwargs.pop('filename', 'export.xlsx')
        super().__init__(*args, **kwargs)
        self.headers['Content-Type'] = 'application/msexcel'
        self.headers['content-disposition'] =  f'attachment;filename={quote(str(f"{filename}"))}'
        # # cross-origin跨域请求需要设置Access-Control-Expose-Headers响应信息
        self.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
>>>>>>> 00428591ab5b1a8bd2060fa6ca606ce24f4363ba
