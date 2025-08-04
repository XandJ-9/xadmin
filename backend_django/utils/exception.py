from django.db.models import ProtectedError, RestrictedError
from django.http import Http404,HttpResponseRedirect
from django.db.utils import DatabaseError
from django.core.exceptions import PermissionDenied

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.status import HTTP_401_UNAUTHORIZED

import logging
import traceback
from .util_response import ErrorResponse

logger = logging.getLogger('django')
def CustomExceptionHandler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = ""
    code = 300
    # 调用默认的异常处理函数
    response = exception_handler(ex, context)
    if isinstance(ex, AuthenticationFailed) or response.status_code == 401:
        # 如果是身份验证错误
        if response and response.data.get("detail") == "Given token not valid for any token type":
            code = 401
            msg = ex.detail
        elif response and response.data.get("detail") == "Token is blacklisted":
            # token在黑名单
            return ErrorResponse(status=HTTP_401_UNAUTHORIZED)
        else:
            code = 401
            msg = ex.detail
            return HttpResponseRedirect(redirect_to='/')
    elif isinstance(ex, Http404):
        code = 404
        msg = "对象不存在"
    elif isinstance(ex, APIException):
        # set_rollback()
        msg = ex.detail
        if isinstance(ex, PermissionDenied):
            msg = f'{msg} ({context["request"].method}: {context["request"].path})'
        if isinstance(msg, dict):
            for k, v in msg.items():
                for i in v:
                    msg = "%s:%s" % (k, i)
    elif isinstance(ex, (ProtectedError, RestrictedError)):
        # set_rollback()
        msg = "无法删除:该条数据与其他数据有相关绑定"
    # elif isinstance(ex, DatabaseError):
    #     set_rollback()
    #     msg = "接口服务器异常,请联系管理员"
    elif isinstance(ex, Exception):
        logger.exception(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg, code=code)
