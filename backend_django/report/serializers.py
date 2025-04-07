from rest_framework import serializers
from system.serializers import BizModelSerializer
from .models import PlatformInfo, ModuleInfo, ReportInfo, InterfaceInfo, InterfaceField

class PlatformInfoSerializer(BizModelSerializer):
    class Meta:
        model = PlatformInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class ModuleInfoSerializer(BizModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    class Meta:
        model = ModuleInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_at', 'update_at','platform']

class ReportInfoSerializer(BizModelSerializer):
    module_name = serializers.CharField(source='module.name', read_only=True)
    platform_name = serializers.CharField(source='module.platform.name', read_only=True)
    class Meta:
        model = ReportInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class InterfaceInfoSerializer(BizModelSerializer):
    class Meta:
        model = InterfaceInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class InterfaceFieldSerializer(BizModelSerializer):
    class Meta:
        model = InterfaceField
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']