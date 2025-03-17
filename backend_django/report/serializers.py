from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict

from .models import  ModuleInfo, PlatformInfo, ReportInfo,Interface, InterfaceField, TableColumn, DataTable

def set_choice_field_internal_value(fields: BindingDict, field_name: str, data: dict):
    field = fields[field_name]
    if not isinstance(field, serializers.ChoiceField):  # 判断是否为ChoiceField
        return 
    if field_name not in data.keys():
        return 
    for internal_value, value in field.choices.items():
        # print(internal_value, value)
        # 将传入的choice字段值修改为数据库中存储的内容
        if data.get(field_name) == value:
            data[field_name]= internal_value


class InterfaceFieldSerializer(serializers.ModelSerializer):
    interface = serializers.SlugRelatedField(queryset=Interface.objects.all(), slug_field='interface_code')
    interface_id = serializers.IntegerField()
    # interface_fields = serializers.HyperlinkedRelatedField(read_only=True, view_name='interface-detail')
    class Meta:
        model = InterfaceField
        fields = '__all__'
    
    def to_internal_value(self, data):
        fields = self.fields
        set_choice_field_internal_value(fields, 'interface_data_type', data)
        set_choice_field_internal_value(fields, 'interface_para_type', data)
        set_choice_field_internal_value(fields, 'interface_export_flag', data)
        set_choice_field_internal_value(fields, 'interface_show_flag', data)
        set_choice_field_internal_value(fields, 'interface_show_desc', data)
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        instance.interface_data_type = InterfaceField.get_interface_data_type_display(instance)
        instance.interface_para_type = InterfaceField.get_interface_para_type_display(instance)
        instance.interface_export_flag = InterfaceField.get_interface_export_flag_display(instance)
        instance.interface_show_flag = InterfaceField.get_interface_show_flag_display(instance)
        instance.interface_show_desc = InterfaceField.get_interface_show_desc_display(instance)
        return super().to_representation(instance)


class InterfaceSerializer(serializers.ModelSerializer):
    # interface_fields = InterfaceFieldSerializer(many=True, read_only=True)
    # interface_fields = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # interface_fields = serializers.SerializerMethodField()
    report = serializers.SlugRelatedField(queryset=ReportInfo.objects.all(), slug_field='name')
    module = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()
    class Meta:
        model = Interface
        fields = '__all__'
    
    def get_module(self, obj):
        report = ReportInfo.objects.get(id=obj.report_id)
        module= ModuleInfo.objects.get(id=report.module_id)
        return module.name
    
    def get_platform(self, obj):
        report = ReportInfo.objects.get(id=obj.report_id)
        module= ModuleInfo.objects.get(id=report.module_id)
        platform = PlatformInfo.objects.get(id=module.platform_id)
        return platform.name


    #     return None
    def to_representation(self, instance):
        '''
        重写to_representation方法，将数据库中存储的is_paging等字段值转换为前端显示的值
        '''
        instance.is_paging = Interface.get_is_paging_display(instance)
        instance.is_second_table = Interface.get_is_second_table_display(instance)
        instance.is_total = Interface.get_is_total_display(instance)
        instance.is_date_option=Interface.get_is_date_option_display(instance)
        instance.is_login_visit=Interface.get_is_login_visit_display(instance)
        instance.alarm_type = Interface.get_alarm_type_display(instance)
        return super().to_representation(instance)

    def to_internal_value(self, data):
        '''
        重写to_internal_value方法，将前端传过来的is_paging等字段值转换为数据库中存储的值
        '''
        fields = self.fields
        set_choice_field_internal_value(fields,'is_paging',data)
        set_choice_field_internal_value(fields,'is_total',data)
        set_choice_field_internal_value(fields,'is_date_option',data)
        set_choice_field_internal_value(fields,'is_second_table',data)
        set_choice_field_internal_value(fields,'is_login_visit',data)
        set_choice_field_internal_value(fields,'alarm_type',data)
        return super().to_internal_value(data)

    

class ReportSerializer(serializers.ModelSerializer):
    # interfaces = serializers.SlugRelatedField(queryset=Interface.objects.all(), many=True, slug_field='interface_code')
    module_name = serializers.SlugRelatedField(queryset=ModuleInfo.objects.all(), slug_field='name')
    module_id = serializers.PrimaryKeyRelatedField(queryset=ModuleInfo.objects.all())
    module_name = serializers.SerializerMethodField()
    platform_name = serializers.SerializerMethodField()
    platform_id = serializers.SerializerMethodField()
    report_id = serializers.IntegerField(source='id')
    report_name = serializers.CharField(source='name')
    # interfaces = InterfaceSerializer(many=True, read_only=True)
    class Meta:
        model = ReportInfo
        fields = '__all__'

    def get_platform_name(self, obj):
        platform_name =None
        try:
            module = ModuleInfo.objects.get(id=obj.module_id)
            platform_name = PlatformInfo.objects.get(id=module.platform_id).name
        except:
            pass
        return platform_name

    def get_platform_id(self, obj):
        platform_id =None
        try:
            module = ModuleInfo.objects.get(id=obj.module_id)
            platform_id = PlatformInfo.objects.get(id=module.platform_id).id
        except:
            pass
        return platform_id
    
    def get_module_name(self, obj):
        module_name =None
        try:
            module_name = ModuleInfo.objects.get(id=obj.module_id).name
        except:
            pass
        return module_name

class ModuleSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset=PlatformInfo.objects.all(), slug_field='name')
    reports = ReportSerializer(many=True, read_only=True)
    class Meta:
        model = ModuleInfo
        fields ='__all__'


class PlatformSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = PlatformInfo
        fields = '__all__'

        
class PlatformModuleReportSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = PlatformInfo
        fields = '__all__'



class DataTableSerializer(serializers.ModelSerializer):
    # update_datetime=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', write_only=True)
    class Meta:
        model = DataTable
        fields ='__all__'

    
class TableColumnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TableColumn
        fields ='__all__'