from rest_framework.decorators import action
from .util_response import ExcelResponse, ErrorResponse, DetailResponse
from openpyxl import Workbook

class ExcelImportExportMixin():
  '''
  导出数据
  '''
  
  @action(methods=['post'], detail=False)
  def export(self, request, *args, **kwargs):
    '''
    导出数据
    '''
    try:
      queryset = self.filter_queryset(self.get_queryset())
      serializer = self.get_serializer(queryset, many=True)
      wb = Workbook()
      st = wb.sheetnames[0]
      resp = ExcelResponse()
      wb.save(resp)
      return resp
    except Exception as e:
      return ErrorResponse(msg=str(e))