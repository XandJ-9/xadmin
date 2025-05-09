from rest_framework import serializers
from system.serializers import BizModelSerializer
from .models import PlatformInfo, ModuleInfo, ReportInfo, InterfaceInfo, InterfaceField


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
    module_info = ModuleInfoSerializer(source='module',read_only=True)
    class Meta:
        model = ReportInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class InterfaceInfoSerializer(BizModelSerializer):
    report_info = ReportInfoSerializer(source='report',read_only=True)
    class Meta:
        model = InterfaceInfo
        fields = '__all__'
        read_only_fields = ['id', 'create_datetime', 'update_datetime']


    
class InterfaceFieldSerializer(BizModelSerializer):
    class Meta:
        model = InterfaceField
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']
    
    def update(self, instance, validated_data):
        # print(f'update instance: {validated_data}')
        return super().update(instance, validated_data)

    def create(self, validated_data):
        # return super().create(validated_data)
        # 重写字段添加方法
        # 先判断是否存在，存在则更新，否则添加
        # print(f'create validated_data: {validated_data}')
        interface_para_code_value = validated_data.pop('interface_para_code')
        interface_para_type_value = validated_data.pop('interface_para_type')
        instance , created = InterfaceField.objects.get_or_create(interface_para_code=interface_para_code_value, interface_para_type=interface_para_type_value, defaults=validated_data)
        if not created:
            self.update(instance, validated_data)
        return instance
