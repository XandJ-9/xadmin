from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,GenericViewSet,ModelViewSet
from rest_framework.decorators import action
from rest_framework import serializers
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

from report.models import Interface,ReportInfo,ModuleInfo,PlatformInfo,InterfaceField
from report.serializers import InterfaceSerializer, ModuleSerializer, PlatformSerializer,ReportSerializer, InterfaceFieldSerializer
from report.utils.util_response import SuccessResponse, DetailResponse
from report.utils.util_datetime import getNowTimestamp
from report.utils.viewset import CustomModelViewSet

from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter, quote_sheetname
from openpyxl.worksheet.table import Table, TableStyleInfo

import requests, jwt, logging, json

logger=logging.getLogger(__name__)


class PlatformViewSet(CustomModelViewSet):
    queryset = PlatformInfo.objects.all()
    serializer_class = PlatformSerializer


class ModuleViewSet(CustomModelViewSet):
    queryset = ModuleInfo.objects.all()
    serializer_class = ModuleSerializer


class ReportViewSet(CustomModelViewSet):
    queryset = ReportInfo.objects.all()
    serializer_class = ReportSerializer

    def get_platform_module_report_list(self, request):
        module_id = request.query_params.get('module_id')
        report_id = request.query_params.get('report_id')
        platform_id = request.query_params.get('platform_id')
        report_list = self.get_queryset()
        logger.debug(f"module_id:{module_id}, report_id:{report_id}, platform_id:{platform_id}")
        if report_id and report_id != '':
            report_list = report_list.filter(id=report_id)
        if module_id and module_id != '':
            module = ModuleInfo.objects.filter(id=module_id)
            report_list = report_list.filter(module__in=module)
        if platform_id and platform_id != '':
            platform = PlatformInfo.objects.filter(id=platform_id)
            modules = ModuleInfo.objects.filter(platform__in=platform)
            report_list = report_list.filter(module__in=modules)

        serializer = self.get_serializer(report_list, many=True)
        
        return DetailResponse(data=serializer.data)

class InterfaceViewSet(CustomModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer

    @action(methods=['post'], detail=False, url_path='list')
    def get_interface_list(self, request):
        name = request.data.get('interface_name', '')
        code = request.data.get('interface_code','')
        platform = request.data.get('platform_id','')
        module = request.data.get('module_id','')
        report = request.data.get('report_id','')
        limit = request.data.get('limit')
        page = request.data.get('page')
        logger.debug(f"name:{name}, code:{code}, platform:{platform}, module:{module}, report:{report}")
        interface_list = self.get_queryset()

        if platform:
            platformInfo = PlatformInfo.objects.filter(id=platform)
            moduleInfo = ModuleInfo.objects.filter(platform__in=platformInfo)
            reportInfo = ReportInfo.objects.filter(module_id__in=moduleInfo)
            interface_list = interface_list.filter(report_id__in=reportInfo)
        if module:
            moduleInfo = ModuleInfo.objects.filter(id=module)
            reportInfo = ReportInfo.objects.filter(module_id__in=moduleInfo)
            interface_list = interface_list.filter(report_id__in=reportInfo)
        if report:
            reportInfo = ReportInfo.objects.filter(id=report)
            interface_list = interface_list.filter(report_id__in=reportInfo)
        if name or code:
            interface_list = interface_list.filter(interface_name__icontains=name, interface_code__icontains=code)
        
        ser = InterfaceSerializer(instance = interface_list, many = True, context={'query_fields':False})
        p = Paginator(ser.data, limit)
        page_data = p.get_page(page).object_list
        return SuccessResponse(data=page_data, total=p.count,page=page,limit=limit)

    @action(methods=['post'], detail=False, url_path='queryData')
    def query_report_data(self, request):
        env_type = request.data.get("env_type")
        if env_type == 1:
            url_prefix = settings.REPORT_INTERFACE_URL_PROD 
        else:
            url_prefix = settings.REPORT_INTERFACE_URL_DEV
            
        if not url_prefix:
            return DetailResponse(msg="未配置接口地址")
        full_url = url_prefix + '?interface_code='+request.data.get('interface_code')
        payload = request.data.get('payload')
        token = request.data.get('token')
        if not token:
            sub = '{ "clientType": 13, "dataStorageModel": 2, "storeId": 15, "tenantId": 197, "userId": 53 }'
            iss = 'qyapitest.qiyucloud.com.cn'
            iat = getNowTimestamp() - 60*60*1
            nbf = getNowTimestamp()- 60*60*1
            exp = getNowTimestamp() + 60*60*5 
            data = {
            "sub":sub,
            "iss":iss,
            "iat":iat,
            "nbf":nbf,
            "exp":exp
            }
            token = jwt.encode(data, settings.JWT_KEY, algorithm='HS256')
        header ={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ token
        }
        # print("token",token)
        resp=requests.post(url=full_url, headers=header, json=payload)
        if resp.status_code == 200:
            return DetailResponse(msg="获取成功", data=resp.json())
        else:
            return DetailResponse(msg="获取失败" + str(resp.content))

class InterfaceFieldViewSet(CustomModelViewSet):
    queryset = InterfaceField.objects.all()
    serializer_class = InterfaceFieldSerializer

    
    @action(methods=['post'], detail=False, url_path='list')
    def get_interface_fields(self, request):
        # queryset = self.queryset.filter(interface_id=self.request.query_params.get('interface_id'))
        # serializer = self.get_serializer(queryset, many=True)
        interface_id = request.data.get('interface_id')
        interface_para_type = request.data.get('interface_para_type',[1,2])
        items = InterfaceField.objects.filter(interface_id=interface_id, interface_para_type__in=interface_para_type)
        ser = self.get_serializer(instance=items, many=True)
        return DetailResponse(data=ser.data)

    @action(methods=['post'], detail=False, url_path='update')
    def update_fields(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            field_values = request.data
            result = []
            for field_value in field_values:
                field=InterfaceField.objects.get(id=field_value.get("id"))
                if field:
                    # ser = self.get_serializer(instance=field,data=field_value)
                    ser = InterfaceFieldSerializer(instance=field, data=field_value)
                else:
                    # ser = self.get_serializer(data=field_value)
                    ser = InterfaceFieldSerializer(data=field_value)
                if ser.is_valid():
                    ser.save()
                    result.append(ser.data)
            return DetailResponse(msg=f"更新{len(result)}个字段完成", data=result)
        else:
            return super().update(request, *args, **kwargs)
