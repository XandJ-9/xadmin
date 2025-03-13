from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'create_time']
        read_only_fields = ['id', 'create_time']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    role_info = RoleSerializer(source='role', read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        source='role',
        queryset=Role.objects.all(),
        required=False,
        write_only=True
    )
    role = serializers.CharField(write_only=True, required=False)

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
        role_name = validated_data.get('role')
        role_instance = Role.objects.get(name=role_name)
        validated_data['role']=role_instance

        return super().update(instance, validated_data)