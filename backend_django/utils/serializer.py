import copy
from rest_framework.request import Request
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict
from rest_framework.fields import SkipField,empty
from rest_framework.relations import PKOnlyObject  # NOQA # isort:skip


from utils.util_str import underline_to_camel_string

def set_choice_field_internal_value(fields:BindingDict, field_name:str, data: dict):
    # for field_name in fields:  这种方式无法获取到field_name
        # print(f'{field_name}')
    field = fields[field_name]
    if not isinstance(field, serializers.ChoiceField):  # 判断是否为ChoiceField
        return 
    for internal_value, value in field.choices.items():
        # 将传入的choice字段值修改为数据库中存储的内容
        if data.get(field_name) == value:
            data[field_name]= internal_value

def set_choice_field_representation(fields:BindingDict, field_name:str, instance):
    field = fields[field_name]
    if not isinstance(field, serializers.ChoiceField):  # 判断是否为ChoiceField
        return
    instance.__dict__[field_name] = field.choices.get(instance.__dict__[field_name])

class ChoiceFieldSerializerMixin:
    '''
     将choice字段的value值转换成对应的label值
    '''
    def to_internal_value(self, data):
        ## 这里有一点迷惑，为什么在这里可以获取到self.fields中的key值，
        ## 在set_choice_field_internal_value方法中却不能这样遍历 self.fields的值到field_name
        ## 参考源码中使用 self._writable_fields
        for field_name in self.fields:
            if field_name not in data.keys():
                continue
            set_choice_field_internal_value(self.fields, field_name, data)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        for field_name in self.fields:
            set_choice_field_representation(self.fields,field_name,instance)
        return super().to_representation(instance)
    
class CamelFieldSerializerMixin:
    '''
    将驼峰风格的字段值对应到下划线字段上
    '''
    def to_internal_value(self, data):
        '''
        将驼峰风格的字段值对应到下划线风格的字段上
        只有显示定义的序列化字段才转换
        '''
        # self._writable_fields字段对应模型字段
        # self._declared_fields字段对应显示序列化类中定义的字段
        for field in self._writable_fields:
            # print(f'{field.field_name}  {field.__class__}')
            source_attrs = field.source.split('.')
            camel_field_name = underline_to_camel_string(field.field_name)
            if camel_field_name not in data.keys():
                continue
            
            source_field_name = source_attrs[0]
            if len(source_attrs) > 1 :
                # 如果对应的字段是外键字段，则获取对应的对象信息
                related_field_atrr = source_attrs[1]
                model = getattr(self.Meta, 'model')
                related_field = model._meta.get_field(source_field_name)
                filter_kwargs = {related_field_atrr: data.pop(camel_field_name)}
                qs = related_field.related_model._default_manager.filter(**filter_kwargs)
                if qs.exists():
                    data[source_field_name] = qs.first()
            else:
                data[source_field_name] = data.pop(camel_field_name)
        # return super().to_internal_value(data)
        return data
    def to_representation(self, instance):
        '''
        将下划线风格字段转换成驼峰风格字段
        '''
        ret = {}
        fields = self._readable_fields

        for field in fields:

            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            except AttributeError as exc:
                # 'read_only', 'write_only',
                # 'required', 'default', 'initial', 'source',
                # 'label', 'help_text', 'style',
                # 'error_messages', 'validators', 'allow_null', 'allow_blank',
                # 'choices'
                # print(f'attribute error: {field.field_name} => {field} => instance is {instance}')
                msg = '`{field_name}` was declared without a `default` or `allow_null=True` or `required=False` argument.'.format(field_name=field.field_name)
                raise type(exc)(msg)

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                # 转换驼峰字段
                camel_field_name = underline_to_camel_string(field.field_name)
                ret[camel_field_name] = field.to_representation(attribute)

        return ret
    

class UpdateSourceFieldSerializerMixin:
    '''
    将自定义字段的值赋值给源字段
    例如定义字段如下：

    parentId  = serializers.IntegerField(source='parent.id')

    将传入数据中的parentId值赋值给parent字段

    如果不想这样，可以在定义时添加参数read_only=True

    parentId  = serializers.IntegerField(source='parent.id')
    '''
    def to_internal_value(self, data):
        # 再通过遍历 declared_fields字段赋值关联字段
        model = getattr(self.Meta, 'model')
        # model_field_info = model_meta.get_field_info(model)
        declared_fields = copy.deepcopy(self._declared_fields)

        for field_name, field in declared_fields.items():
            if field.source == '*':
                source_attrs = []
            else:
                source_attrs = field.source.split('.')

            if field.read_only:  # 跳过只读字段
                continue
            if len(source_attrs) > 0:
                # 向data中添加关联字段的值
                # print(f'update {field_name}:({source_attrs[0]}) =  {data.get(field_name,None)}')
                data.update({source_attrs[0]: data.get(field_name,None)})

        return super().to_internal_value(data)
    

class BizModelSerializer(serializers.ModelSerializer):
    """adding creator and updator fields to serializers."""
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='created_at')
    updator_username = serializers.CharField(source='updator.username', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source='updated_at')
    
    def __init__(self, instance=None, data=empty, request=None, **kwargs):
            super().__init__(instance, data, **kwargs)
            self.request: Request = request or self.context.get("request", None)