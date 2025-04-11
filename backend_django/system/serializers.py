from rest_framework import serializers
from .models import User,Role,Menu, SystemConfig


class RoleSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'create_time']
        read_only_fields = ['id', 'create_time']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='created_at')
    role_info = RoleSerializer(source='role', read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=Role.objects.all(),
        required=False,
        write_only=True
    )
    role = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role_info', 'role_id', 'create_time', 'role']
        read_only_fields = ['id', 'create_time']

    def create(self, validated_data):
        role_instance = Role.objects.get(name=validated_data.get('role'))
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role_instance
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        if 'role' in validated_data:
            role_name = validated_data.get('role')
            role_instance = Role.objects.get(name=role_name)
            validated_data['role']=role_instance

        return super().update(instance, validated_data)

class MenuSerializer(serializers.ModelSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    meta = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'name_code', 'parent', 'parent_name', 'path', 'component', 'redirect', 
                 'icon', 'sort', 'hidden', 'meta', 'creator', 'creator_info', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_meta(self, obj):
        """返回meta对象，包含前端路由需要的meta信息"""
        return {
            'title': obj.meta_title or obj.name,
            'icon': obj.meta_icon or obj.icon
        }

class SystemConfigSerializer(serializers.ModelSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'creator', 'creator_info', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BizModelSerializer(serializers.ModelSerializer):
    """adding creator and updator fields to serializers."""
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='created_at')
    updator_username = serializers.CharField(source='updator.username', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='updated_at')
    
    # def create(self, validated_data):
    #     # validated_data['creator'] = self.context['request'].user
    #     # validated_data['updator'] = self.context['request'].user
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     # validated_data['updator'] = self.context['request'].user
    #     return super().update(instance, validated_data)