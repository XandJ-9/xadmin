from rest_framework import serializers
from .models import User,Role,Menu, SystemConfig, Dept, SystemDictType,SystemDictData
from utils.serializer import ChoiceFieldSerializerMixin, CamelFieldSerializerMixin,UpdateSourceFieldSerializerMixin,BizModelSerializer



class SystemBaseSerializer(CamelFieldSerializerMixin,BizModelSerializer):
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
    deptName = serializers.CharField(source='dept_name',read_only=True)
    orderNum = serializers.IntegerField(source='order_num',read_only=True)
    parentId = serializers.IntegerField(source='parent.id', read_only=True)
    class Meta:
        model = Dept
        fields = '__all__'
        # fields = ['id','deptId', 'deptName', 'orderNum', 'status','parent']
        read_only_fields = ['id', 'create_time','update_time','creator','updator']
    
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
    deptId = serializers.IntegerField(source="dept.id",read_only=True,required=False)
    password = serializers.CharField(write_only=True, required=False)
    dept = DeptSerializer(read_only=True)

    class Meta:
        model = User
        # fields = ['user_id', 'username','nickname', 'sex','password', 'dept', 'create_time','avatar','status','phonenumber','dept_id']
        fields = '__all__'
        read_only_fields = ['id', 'create_time']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        instance.set_password(password)  # Set the password using set_password method
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        if 'role' in validated_data:
            role_name = validated_data.get('role')
            role_instance = Role.objects.get(name=role_name)
            validated_data['role']=role_instance

        return super().update(instance, validated_data)

class MenuSerializer(UpdateSourceFieldSerializerMixin,SystemBaseSerializer):
    menuId = serializers.IntegerField(source='id', read_only=True)
    parentId  = serializers.IntegerField(source='parent.id', required=False)
    
    class Meta:
        model = Menu
        fields = "__all__"
        # exclude = ['creator','updator','created_at', 'updated_at']
        read_only_fields = ['id']

class SystemConfigSerializer(SystemBaseSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)
    
    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'creator', 'creator_info', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']




