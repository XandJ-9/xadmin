from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,GenericViewSet,ModelViewSet
from rest_framework.decorators import action
from rest_framework import serializers

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

from report.utils.viewset import CustomModelViewSet
from report.models import DataTable, TableColumn, TableColumnMapping, TableMapping
from report.utils.util_response import SuccessResponse, DetailResponse
from report.utils.filters import SearchFilterBackend
from report.utils.util_spark import list_database, start_spark,stop_spark
from report.serializers import DataTableSerializer, TableColumnSerializer




class TableView(CustomModelViewSet):
    queryset = DataTable.objects.all()
    serializer_class = DataTableSerializer
    filter_backends = [SearchFilterBackend]
    filter_fields = ['table_name','table_desc']


    @action(methods=['post'], detail=False, url_path="list")
    def get_table_list(self, request):
        pageSize = request.data.get('limit')
        currentPage = request.data.get('page')
        table_name = request.data.get('table_name')
        table_comment = request.data.get('table_comment')
        objs = DataTable.objects.filter(Q(table_name__contains=table_name)|Q(table_desc__contains=table_comment))
        # return DetailResponse(msg="获取元数据-表信息", data=ser.data)
        p =Paginator(objs, pageSize)
        objs = p.get_page(currentPage).object_list
        ser = DataTableSerializer(objs, many=True)
        return SuccessResponse(msg="获取元数据-表信息",data=ser.data,total=p.count,page=currentPage,limit=pageSize)

    
    @action(methods=['post'], detail=False, url_path='detail')
    def get_table_detail(self, request):
        table_id =request.data.get("table_id")
        obj = TableColumn.objects.filter(table_id = table_id)
        ser = TableColumnSerializer(obj, many=True)
        return DetailResponse(msg="获取元数据-字段信息", data = ser.data)
    
class TableColumnView(CustomModelViewSet):
    authentication_classes = []
    queryset = TableColumn.objects.all()
    serializer_class = TableColumnSerializer


class DatabaseView(CustomModelViewSet):
    authentication_classes = []

    def list(self, request):
        start_spark()
        # start_spark_remote()
        db_list = list_database()
        stop_spark()
        result = []
        for item in db_list:
            tmp = {}
            tmp['name']= item.name
            tmp['description']= item.description
            result.append(tmp)
        return DetailResponse(msg ='获取元数据-数据库信息', data=result)


class TableMappingView(CustomModelViewSet):
    queryset = TableMapping.objects.all()
    serializer_class = serializers.ModelSerializer

    class Meta:
        model = TableMapping
        fields = '__all__'

    @action(methods=['post'], detail=False, url_path='list')
    def get_mapping_list(self, request):
        table_id = request.data.get('table_id')
        table_name = request.data.get('table_name')
        schema_type = request.data.get('schema_type')
        
        mappings = self.get_queryset()
        if table_id:
            mappings = mappings.filter(table_id=table_id)
        if table_name:
            mappings = mappings.filter(table_name__icontains=table_name)
        if schema_type:
            mappings = mappings.filter(schema_type=schema_type)
            
        serializer = self.get_serializer(mappings, many=True)
        return DetailResponse(msg='获取表映射信息', data=serializer.data)

class TableColumnMappingView(CustomModelViewSet):
    queryset = TableColumnMapping.objects.all()
    serializer_class = serializers.ModelSerializer

    class Meta:
        model = TableColumnMapping
        fields = '__all__'

    @action(methods=['post'], detail=False, url_path='list')
    def get_column_mapping_list(self, request):
        table_id = request.data.get('table_id')
        
        mappings = self.get_queryset()
        if table_id:
            mappings = mappings.filter(table_id=table_id)
            
        serializer = self.get_serializer(mappings, many=True)
        return DetailResponse(msg='获取字段映射信息', data=serializer.data)
