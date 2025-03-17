from rest_framework import serializers
from .models import PlatformInfo, ModuleInfo, ReportInfo, InterfaceInfo, InterfaceField

class PlatformInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class ModuleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class ReportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class InterfaceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceInfo
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']

class InterfaceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfaceField
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'create_datetime', 'update_datetime']