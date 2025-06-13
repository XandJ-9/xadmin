from rest_framework import serializers
from system.serializers import BizModelSerializer
from .models import DataSource, QueryLog

class DataSourceSerializer(BizModelSerializer):
    datasource_name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = DataSource
        fields = '__all__'
        # fields = ['id', 'name', 'type', 'host', 'port', 'database', 'username', 
                #  'password', 'description', 'creator', 'creator_username', 
                #  'create_at','updator_username', 'update_at']
        read_only_fields = ['id', 'creator', 'create_at', 'update_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation.pop('password', None)
        return representation


class QueryLogSerializer(BizModelSerializer):
    datasource_name = serializers.CharField(source='datasource.name', read_only=True)
    username = serializers.CharField(source='creator.username', read_only=True)
    execution_time = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = QueryLog
        fields = '__all__'
        # fields = ['id', 'datasource', 'datasource_name', 'creator', 'username', 'sql', 
                #  'status', 'error_message', 'execution_time', 'result_count', 'create_time','creator_username']
        read_only_fields = ['id', 'created_at']