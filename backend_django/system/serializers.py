from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.fields import empty
from .models import *
from utils.serializer import ChoiceFieldSerializerMixin, CamelFieldSerializerMixin,UpdateSourceFieldSerializerMixin,BaseModelSerializer
from django.contrib.auth.hashers import make_password



class SystemBaseSerializer(CamelFieldSerializerMixin,BaseModelSerializer):
    pass


class SystemDictTypeSerializer(SystemBaseSerializer):
    dictId = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = SystemDictType
        fields = "__all__"

class SystemDictDataSerializer(SystemBaseSerializer):
    dictId = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = SystemDictData
        fields = "__all__"




class DeptSerializer(SystemBaseSerializer):
    deptId = serializers.IntegerField(source='id', read_only=True)
    parentId = serializers.IntegerField(source='parent.id', required=False)
    class Meta:
        model = Dept
        fields = ['id','deptId', 'dept_name', 'order_num', 'status','parentId',"ancestors","creator_username", "parent"]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        # 设置ancestors字段的值
        parent = validated_data.get('parent', None)
        if parent:
            ancestors = ','.join([parent.ancestors, str(parent.id)])
        else:
            ancestors = '0'
        validated_data['ancestors'] = ancestors
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # 更新ancestors字段的值
        parent = validated_data.get('parent', None)
        if parent:
            ancestors = ','.join([parent.ancestors, str(parent.id)])
        else:
            ancestors = '0'
        validated_data['ancestors'] = ancestors
        return super().update(instance, validated_data)
    

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
    password = serializers.CharField(write_only=True, allow_blank=False, required=False)
    # dept = DeptSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['userId', 'username','nickname', 'sex', 'create_time','avatar','status','phonenumber','email','dept','deptId','creator_username','updator_username','password']
        read_only_fields = ['id']
        write_only_fields = ['password','dept']

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

class UserPostSerializer(SystemBaseSerializer):
    class Meta:
        model = UserPost
        fields = ['id', 'user', 'post','creator','updator']

class MenuSerializer(SystemBaseSerializer):
    menuId = serializers.IntegerField(source='id', read_only=True)
    parentId  = serializers.IntegerField(source='parent.id', required=False)
    
    class Meta:
        model = Menu
        # fields = "__all__"
        exclude = ['creator','updator','created_at', 'updated_at','id']
        read_only_fields = ['id']

class RoleMenuSerializer(SystemBaseSerializer):
    class Meta:
        model = RoleMenu
        fields = ['id', 'role', 'creator', 'updator','menu']
        read_only_fields = ['id']

class RoleSerializer(SystemBaseSerializer):
    roleId = serializers.IntegerField(source='id', read_only=True) 
    # roleKey = serializers.CharField(source='role_key', read_only=True)
    # roleName =  serializers.CharField(source='role_name', read_only=True)
    menuIds = serializers.SerializerMethodField()

    def get_menuIds(self, obj):
        return obj.role_menus.all().values_list('menu_id', flat=True)

    def create(self, validated_data):
        menu_ids = validated_data.pop('menuIds', [])
        role = Role.objects.create(**validated_data)
        role.role_menus.set(menu_ids)
        return role
    def update(self, instance, validated_data):
        # menu_ids = validated_data.pop('menuIds', [])
        menu_ids = self.initial_data.pop('menuIds', [])
        instance = super().update(instance, validated_data)
        for menuId in menu_ids:
            menu = Menu.objects.get(id=menuId)
            RoleMenu.objects.get_or_create(role=instance, menu=menu)
        return instance
    
    class Meta:
        model = Role
        fields = ['roleId', 'role_key','role_name', 'create_time','status','role_sort','menuIds']
        read_only_fields = ['id', 'create_time']

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

