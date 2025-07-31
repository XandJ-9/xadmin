from rest_framework.decorators import action
from django.http.response import HttpResponseNotFound,HttpResponseServerError

from utils.util_response import DetailResponse, ExcelResponse
from system.models import UploadFileInfo
from report.models import *
from .operation_excel import generate_interface_workbook, handle_import_interface, handle_import_tableinfo
from hashlib import md5

import logging 

logger = logging.getLogger('django')



class ExcelImportExportMixin:

    @action(methods=['post'], detail=False)
    def import_interfaceinfo(self, request, *args, **kwargs):
        """
        Import interface information from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        try:
            file_obj = request.FILES['file']
            # logger.info(uploadfile._name)
            # full_filepath = os.path.join(settings.IMPORT_FILE_PATH,file._name)
            # with open(full_filepath,'wb+') as outfile:
                # for chunk in uploadfile.chunks():
                    # outfile.write(chunk)
            file_md5 = md5(file_obj.read()).hexdigest()
            upload_file, created = UploadFileInfo.objects.get_or_create(file_md5=file_md5, 
                                                                        defaults={
                                                                            'source_file_name': file_obj.name,
                                                                            'file': file_obj,
                                                                            'file_size': file_obj.size,
                                                                            'biz_type': '1'
                                                                        })
            if not created:
                upload_file.source_file_name = file_obj.name
                upload_file.file = file_obj
                upload_file.file_size = file_obj.size
                upload_file.biz_type = '1'
                upload_file.creator = request.user
                upload_file.updator = request.user
                upload_file.save()
            handle_import_interface(upload_file.file.name, request.user)
            return DetailResponse(
            msg='文件导入成功',
            status=200,
            )
        except Exception as e:
            logger.error(e)
            return HttpResponseServerError(content=f'导入失败 {e}')

    @action(methods=['post'], detail=False)
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
            # interface_data = InterfaceInfoExportSerializer(interface).data
            interface_data = self.get_serializer(interface).data
            wb = generate_interface_workbook(interface_data, fields)
            response = ExcelResponse(filename=f"{interface.report}-{interface.interface_name}.xlsx", workbook = wb)
            return response
        except Exception as e:
            logger.error(e)
            return HttpResponseNotFound(content='导出接口失败')
    

    @action(methods=['post'], detail=False, url_path='import/Tablemapping', url_name='import_tablemapping')
    def import_tablemapping(self, request, *args, **kwargs):
        """
        Import table mapping from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        pass

    @action(methods=['post'], detail=False, url_path='import/Tableinfo', url_name='import_tableinfo')
    def import_tableinfo(self, request, *args, **kwargs):
        """
        Import table information from an Excel file.
        """
        # Implement the logic to read the Excel file and import data
        file_obj = request.FILES['file']
        # logger.info(uploadfile._name)
        # full_filepath = os.path.join(settings.IMPORT_FILE_PATH,file._name)
        # with open(full_filepath,'wb+') as outfile:
            # for chunk in uploadfile.chunks():
                # outfile.write(chunk)
        file_md5 = md5(file_obj.read()).hexdigest()
        upload_file, created = UploadFileInfo.objects.get_or_create(file_md5=file_md5, 
                                                                    defaults={
                                                                        'source_file_name': file_obj.name,
                                                                        'file': file_obj,
                                                                        'file_size': file_obj.size,
                                                                        'biz_type': '2'
                                                                    })
        if not created:
            upload_file.source_file_name = file_obj.name
            upload_file.file = file_obj
            upload_file.file_size = file_obj.size
            upload_file.biz_type = '1'
            upload_file.creator = request.user
            upload_file.updator = request.user
            upload_file.save()
        handle_import_tableinfo(upload_file.file.name, request.user)
        return DetailResponse(msg='Import table information from Excel file', status=200)

        

