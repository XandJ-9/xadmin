from utils.viewset import CustomModelViewSet
from .models import PlatformInfo, ModuleInfo, ReportInfo, InterfaceInfo, InterfaceField,InterfaceQueryLog
from .serializers import *
from .utils.mixin_excel_import_export import ExcelImportExportMixin
from .utils.mixin_interface_query import InterfaceQueryMixin 

class PlatformInfoViewSet(CustomModelViewSet):
    queryset = PlatformInfo.objects.all()
    serializer_class = PlatformInfoSerializer
    search_fields = ['name', 'desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class ModuleInfoViewSet(CustomModelViewSet):
    queryset = ModuleInfo.objects.all()
    serializer_class = ModuleInfoSerializer
    filterset_fields = ['platform']
    search_fields = ['name', 'desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class ReportInfoViewSet(CustomModelViewSet):
    queryset = ReportInfo.objects.all()
    serializer_class = ReportInfoSerializer
    filterset_fields = ['module']
    search_fields = ['name', 'desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class InterfaceInfoViewSet(CustomModelViewSet):
    queryset = InterfaceInfo.objects.all()
    serializer_class = InterfaceInfoSerializer
    filterset_fields = ['report_id', 'interface_code', 'interface_name']
    search_fields = ['interface_name', 'interface_code', 'interface_desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class InterfaceFieldViewSet(CustomModelViewSet):
    queryset = InterfaceField.objects.all()
    serializer_class = InterfaceFieldSerializer
    filterset_fields = ['interface']
    filter_fields = ['interface_para_code','interface_para_name']

class InterfaceImportExportViewSet(ExcelImportExportMixin, CustomModelViewSet):
    queryset = None
    serializer_class = InterfaceInfoImportExportSerializer

    def generate_export_file(self, request, *args, **kwargs):
        pass


class InterfaceQueryViewSet(InterfaceQueryMixin, CustomModelViewSet):
    '''
    接口查询视图
    '''
    queryset = None


class InterfaceQueryLogViewSet(CustomModelViewSet):
    '''
    接口查询日志视图
    '''
    queryset = InterfaceQueryLog.objects.all()
    serializer_class = InterfaceQueryLogSerializer