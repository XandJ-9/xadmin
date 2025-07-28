from abc import abstractmethod
from utils.util_response import DetailResponse, ExcelResponse
from hashlib import md5
from report.models import UploadFileInfo

class ExcelImportExportMixin:
    export_serializer_class = None
    import_serializer_class = None
    filename = 'excel_file'

    @abstractmethod
    def create_excel_file(self, data, output_file_name = None):
        raise NotImplementedError('请实现create_excel_file方法')
    
    def export_data(self, request, *args, **kwargs):
        try:
          serializer = self.get_export_serializer(request, *args, **kwargs)
          wb = self.create_excel_file(serializer.data)
          response = ExcelResponse(filename=f"{self.filename}.xlsx", workbook = wb)
          return response
        except Exception as e:
            return DetailResponse(msg=str(e))
    
    @abstractmethod
    def parse_import_file(self, request, *args, **kwargs):
        raise NotImplementedError('请实现parse_import_file方法')
    def import_data(self, request, *args, **kwargs):
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
            self.parse_import_file(upload_file.file.name, request.user)
            return DetailResponse(
            msg='文件导入成功',
            status=200,
            )
      except Exception as e:
            return DetailResponse(msg=f'导入失败 {e}')