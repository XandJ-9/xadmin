from rest_framework.decorators import action
from django.http.response import HttpResponseNotFound, HttpResponse
from urllib.parse import quote
from django.conf import settings

from utils.util_response import DetailResponse
from ..models import *
from report.common.excel_operations import generate_interface_workbook, handle_interface_import

import os,logging 

logger = logging.getLogger('django')

class ExcelResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        filename = kwargs.pop('filename', 'export.xlsx')
        super().__init__(*args, **kwargs)
        self.headers['Content-Type'] = 'application/msexcel'
        self.headers['content-disposition'] =  f'attachment;filename={quote(str(f"{filename}"))}'
        # # cross-origin跨域请求需要设置Access-Control-Expose-Headers响应信息
        self.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'


class ExcelImportExportMixin:

    @action(methods=['post'], detail=False, url_path='importInterfaceinfo', url_name='import_interfaceinfo')
    def import_interfaceinfo(self, request, *args, **kwargs):
        """
        Import interface information from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        try:
            uploadfile = request.FILES['file']
            full_filepath = os.path.join(settings.IMPORT_FILE_PATH,uploadfile._name)
            with open(full_filepath,'wb+') as outfile:
                for chunk in uploadfile.chunks():
                    outfile.write(chunk)
            handle_interface_import(full_filepath, request.user)
        except Exception as e:
            logger.error(e)
            raise e
        return DetailResponse(
            msg='Import interface information from Excel file',
            status=200,
        )

    @action(methods=['post'], detail=False, url_path='exportInterfaceinfo', url_name='export_interfaceinfo')
    def export_interfaceinfo(self, request, *args, **kwargs):
        """
        Export interface information to an Excel file.
        """
        # Implement the logic to export data to an Excel file
        interface_id = request.query_params.get('interface_id')
        try:
            interface = InterfaceInfo.objects.get(id = interface_id)
        
            fields = InterfaceField.objects.filter(interface_id = interface_id)
            if not fields:
                fields = None
            response = ExcelResponse(filename=f"{interface.report}-{interface.interface_name}.xlsx")
            wb = generate_interface_workbook(interface, fields)
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

