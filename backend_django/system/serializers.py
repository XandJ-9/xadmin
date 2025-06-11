from rest_framework.request import Request
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.utils import model_meta
from .models import User,Role,Menu, SystemConfig, Dept, SystemDictType,SystemDictData
from utils.serializer import ChoiceFieldSerializerMixin, CamelFieldSerializerMixin
import copy

class BizModelSerializer(CamelFieldSerializerMixin,serializers.ModelSerializer):
    """adding creator and updator fields to serializers."""
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='created_at')
    updator_username = serializers.CharField(source='updator.username', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='updated_at')
    
    def __init__(self, instance=None, data=empty, request=None, **kwargs):
            super().__init__(instance, data, **kwargs)
            self.request: Request = request or self.context.get("request", None)

    def to_internal_value(self, data):
        # 再通过遍历 declared_fields字段赋值关联字段
        model = getattr(self.Meta, 'model')
        model_field_info = model_meta.get_field_info(model)
        declared_fields = copy.deepcopy(self._declared_fields)
        # print(f'declared_fields: {declared_fields}')
        for field_name, field in declared_fields.items():
            if not field.source in model_field_info.relations:  # 判断是否为关联字段
                continue
            relation_info = model_field_info.relations[field.source]
            # print(f'{field_name}  =>  {field}  => {relation_info}')
        # 向data中添加关联字段的值

        return super().to_internal_value(data)

class SystemDictTypeSerializer(BizModelSerializer):
    create_time = serializers.DateTimeField(source='created_at',format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = SystemDictType
        fields = "__all__"

class SystemDictDataSerializer(BizModelSerializer):
    class Meta:
        model = SystemDictData
        fields = "__all__"

class RoleSerializer(BizModelSerializer):
    roleId = serializers.IntegerField(source='id', read_only=True) 
    roleKey = serializers.CharField(source='role_key', read_only=True)
    roleName =  serializers.CharField(source='role_name', read_only=True)
    class Meta:
        model = Role
        fields = ['roleId', 'roleKey','roleName', 'create_time','status']
        read_only_fields = ['id', 'create_time']

class DeptSerializer(BizModelSerializer):
    deptId = serializers.IntegerField(source='id', read_only=True)
    deptName = serializers.CharField(source='dept_name',read_only=True)
    orderNum = serializers.IntegerField(source='order_num',read_only=True)
    parentId = serializers.IntegerField(source='parent.id', read_only=True)
    class Meta:
        model = Dept
        fields = '__all__'
        # fields = ['id','deptId', 'deptName', 'orderNum', 'status','parent']
        read_only_fields = ['id', 'create_time','update_time','creator','updator']
    
class UserExportSerializer(BizModelSerializer):
    dept_name = serializers.CharField(source="dept.dept_name", read_only=True)
    class Meta:
        model = User 
        fields = ['username','nickname','phonenumber','email','sex','status','dept_name','create_time']

class UserImportSerializer(ChoiceFieldSerializerMixin,BizModelSerializer):
    dept_name = serializers.CharField(source="dept.dept_name", read_only=True)
    class Meta:
        model = User
        fields = ['id','username','nickname','phonenumber','email','sex','status','dept_name','create_time']

class UserSerializer(BizModelSerializer):
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

class MenuSerializer(BizModelSerializer):
    menuId = serializers.IntegerField(source='id', read_only=True)
    parentId  = serializers.IntegerField(source='parent.id', read_only=True)  # 想办法通过传递parentId的值来修改模型字段parent的值，对应模型中parent_id
    
    class Meta:
        model = Menu
        # fields = "__all__"
        exclude = ['creator','updator','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SystemConfigSerializer(BizModelSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)
    
    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'creator', 'creator_info', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']




