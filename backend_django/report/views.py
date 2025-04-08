from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utils.viewset import CustomModelViewSet
from .models import PlatformInfo, ModuleInfo, ReportInfo, InterfaceInfo, InterfaceField
from .serializers import (
    PlatformInfoSerializer,
    ModuleInfoSerializer,
    ReportInfoSerializer,
    InterfaceInfoSerializer,
    InterfaceFieldSerializer
)
from .common.excel_import_export import ExcelImportExportMixin


class PlatformInfoViewSet(CustomModelViewSet):
    queryset = PlatformInfo.objects.all()
    serializer_class = PlatformInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class ModuleInfoViewSet(CustomModelViewSet):
    queryset = ModuleInfo.objects.all()
    serializer_class = ModuleInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['platform']
    search_fields = ['name', 'desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class ReportInfoViewSet(CustomModelViewSet):
    queryset = ReportInfo.objects.all()
    serializer_class = ReportInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['module']
    search_fields = ['name', 'desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class InterfaceInfoViewSet(ExcelImportExportMixin,CustomModelViewSet):
    queryset = InterfaceInfo.objects.all()
    serializer_class = InterfaceInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['report', 'interface_db_type', 'is_total', 'is_paging', 'is_date_option', 'is_second_table', 'is_login_visit', 'alarm_type']
    search_fields = ['interface_name', 'interface_code', 'interface_desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime']

class InterfaceFieldViewSet(CustomModelViewSet):
    queryset = InterfaceField.objects.all()
    serializer_class = InterfaceFieldSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['interface']
    search_fields = ['field_name', 'field_code', 'field_desc']
    ordering_fields = ['id', 'create_datetime', 'update_datetime', 'field_order']