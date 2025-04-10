from rest_framework.decorators import action
from django.http.response import HttpResponseNotFound, HttpResponse 
from urllib.parse import quote
from openpyxl import Workbook

from utils.util_response import DetailResponse
from ..models import *


import logging 

logger = logging.getLogger('django')

class ExcelResponse(HttpResponse):
    def __init__(self, content = ..., *args, **kwargs):
        filename = kwargs.pop('filename', 'export.xlsx')
        super().__init__(content, *args, **kwargs)
        self['content_type'] = 'application/msexcel'
        self['Content-Disposition'] =  f'attachment;filename={quote(str(f"{filename}"))}'
        self['Access-Control-Expose-Headers'] = 'Content-Disposition'


class ExcelImportExportMixin:

    @action(methods=['post'], detail=False, url_path='importInterfaceinfo', url_name='import_interfaceinfo')
    def import_interfaceinfo(self, request, *args, **kwargs):
        """
        Import interface information from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        return DetailResponse(
            msg='Import interface information from Excel file',
            status=200,
        )

    @action(methods=['post'], detail=False, url_path='exportInterfaceinfo', url_name='export_interfaceinfo'
            ,permission_classes=[]
            ,authentication_classes=[])
    def export_interfaceinfo(self, request, *args, **kwargs):
        """
        Export interface information to an Excel file.
        """
        # Implement the logic to export data to an Excel file
        interface_id = request.query_params.get('interface_id')
        try:
            instance = InterfaceInfo.objects.get(id = interface_id)
        

            # 设置返回类型为Excel
            # response = HttpResponse(content_type="application/msexcel")
            # # cross-origin跨域请求需要设置Access-Control-Expose-Headers响应信息
            # response["Access-Control-Expose-Headers"] = f"Content-Disposition"
            # # 设置文件名
            # response["content-disposition"] = f'attachment;filename={quote(str(f"{instance.report}-{instance.interface_name}.xlsx"))}'
            response = ExcelResponse(filename=f"{instance.report}-{instance.interface_name}.xlsx")
            # wb = generate_interface_workbook(interface_id)
            wb = Workbook()
            wb.save(response)
            return response
        except Exception as e:
            logger.error(e)
            return HttpResponseNotFound(content='接口不存在')
    

    @action(methods=['post'], detail=False, url_path='importTablemapping', url_name='import_tablemapping')
    def import_tablemapping(self, request, *args, **kwargs):
        """
        Import table mapping from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        pass

    @action(methods=['post'], detail=False, url_path='importTableinfo', url_name='import_tableinfo')
    def import_tableinfo(self, request, *args, **kwargs):
        """
        Import table information from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        pass

