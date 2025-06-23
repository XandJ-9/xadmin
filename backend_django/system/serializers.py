from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.fields import empty
from .models import *
from utils.serializer import ChoiceFieldSerializerMixin, CamelFieldSerializerMixin,UpdateSourceFieldSerializerMixin,BaseModelSerializer



class SystemBaseSerializer(CamelFieldSerializerMixin,BaseModelSerializer):
    pass


class SystemDictTypeSerializer(SystemBaseSerializer):
    dictId = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = SystemDictType
        fields = "__all__"

class SystemDictDataSerializer(SystemBaseSerializer):
    class Meta:
        model = SystemDictData
        fields = "__all__"

class RoleSerializer(SystemBaseSerializer):
    roleId = serializers.IntegerField(source='id', read_only=True) 
    roleKey = serializers.CharField(source='role_key', read_only=True)
    roleName =  serializers.CharField(source='role_name', read_only=True)
    class Meta:
        model = Role
        fields = ['roleId', 'roleKey','roleName', 'create_time','status']
        read_only_fields = ['id', 'create_time']

class DeptSerializer(SystemBaseSerializer):
    deptId = serializers.IntegerField(source='id', read_only=True)
    parentId = serializers.IntegerField(source='parent.id', required=False)
    class Meta:
        model = Dept
        fields = ['id','deptId', 'dept_name', 'order_num', 'status','parentId',"ancestors","creator_username", "parent"]
        read_only_fields = ['id','parent']
    
class UserExportSerializer(SystemBaseSerializer):
    dept_name = serializers.CharField(source="dept.dept_name", read_only=True)
    class Meta:
        model = User 
        fields = ['username','nickname','phonenumber','email','sex','status','dept_name','create_time']

class UserImportSerializer(ChoiceFieldSerializerMixin,SystemBaseSerializer):
    dept_name = serializers.CharField(source="dept.dept_name", read_only=True)
    class Meta:
        model = User
        fields = ['id','username','nickname','phonenumber','email','sex','status','dept_name','create_time']

class UserSerializer(SystemBaseSerializer):
    userId = serializers.IntegerField(source="id",read_only=True,required=False)
    deptId = serializers.IntegerField(source="dept.id",required=False)
    password = serializers.CharField(write_only=True, allow_blank=False)
    dept = DeptSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['userId', 'username','nickname', 'sex','password', 'dept', 'create_time','avatar','status','phonenumber','email','deptId','creator_username','updator_username']
        # read_only_fields = ['id', 'create_time']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        instance.set_password(password)  # Set the password using set_password method
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data.get('password', None):
            password = validated_data.pop('password')
            instance.check_password(password)
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserRoleSerializer(SystemBaseSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role','creator','updator']

class MenuSerializer(UpdateSourceFieldSerializerMixin,SystemBaseSerializer):
    menuId = serializers.IntegerField(source='id', read_only=True)
    parentId  = serializers.IntegerField(source='parent.id', required=False)
    
    class Meta:
        model = Menu
        fields = "__all__"
        # exclude = ['creator','updator','created_at', 'updated_at']
        read_only_fields = ['id']

class RoleMenuSerializer(SystemBaseSerializer):
    class Meta:
        model = RoleMenu
        fields = ['id', 'role', 'menu', 'creator', 'updator']
        read_only_fields = ['id']

class SystemConfigSerializer(SystemBaseSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)
    
    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'creator', 'creator_info', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PostSerializer(SystemBaseSerializer):
    postId = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Post
        fields = ['postId', 'post_code', 'post_name', 'post_sort', 'status', 'remark', 'create_time', 'update_time','creator_username']

