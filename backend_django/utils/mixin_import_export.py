from rest_framework.decorators import action


class Mixin_Export():
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
      return SuccessResponse(data=serializer.data)
    except Exception as e:
      return ErrorResponse(msg=str(e))