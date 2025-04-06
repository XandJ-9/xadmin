from rest_framework import serializers
from .models import DataSource, QueryLog

class DataSourceSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DataSource
        fields = ['id', 'name', 'type', 'host', 'port', 'database', 'username', 
                 'password', 'description', 'creator', 'creator_username', 
                 'create_time', 'update_time']
        read_only_fields = ['id', 'creator', 'create_time', 'update_time']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation.pop('password', None)
        return representation


class QueryLogSerializer(serializers.ModelSerializer):
    datasource_name = serializers.CharField(source='datasource.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = QueryLog
        fields = ['id', 'datasource', 'datasource_name', 'user', 'username', 'sql', 
                 'status', 'error_message', 'execution_time', 'result_count', 'created_at']
        read_only_fields = ['id', 'created_at']