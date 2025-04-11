from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict
from system.serializers import BizModelSerializer
from .models import PlatformInfo, ModuleInfo, ReportInfo, InterfaceInfo, InterfaceField

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

def set_choice_field_representation(fields: BindingDict, field_name: str ,instance):
    field = fields[field_name]
    if not isinstance(field, serializers.ChoiceField):  # 判断是否为ChoiceField
        return
    instance.__dict__[field_name] = field.choices.get(instance.__dict__[field_name])
        

class PlatformInfoSerializer(BizModelSerializer):
    class Meta:
        model = PlatformInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class ModuleInfoSerializer(BizModelSerializer):
    # platform_name = serializers.CharField(source='platform.name', read_only=True)
    platform_info = PlatformInfoSerializer(source='platform', read_only=True)
    class Meta:
        model = ModuleInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_at', 'update_at']

class ReportInfoSerializer(BizModelSerializer):
    # module_name = serializers.CharField(source='module.name', read_only=True)
    # platform_name = serializers.CharField(source='module.platform.name', read_only=True)
    module_info = ModuleInfoSerializer(source='module', read_only=True)
    class Meta:
        model = ReportInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class InterfaceInfoSerializer(BizModelSerializer):
    report_info = ReportInfoSerializer(source='report', read_only=True)
    class Meta:
        model = InterfaceInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

    def to_internal_value(self, data):
        for field_name in data.keys():
            # 获取 选项类型内部实际存储的值
            set_choice_field_internal_value(self.fields, field_name, data)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        for field_name in self.fields.keys():
            set_choice_field_representation(self.fields, field_name ,instance)
        return super().to_representation(instance)
    
class InterfaceFieldSerializer(BizModelSerializer):
    class Meta:
        model = InterfaceField
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']