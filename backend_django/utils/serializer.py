import re
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject  # NOQA # isort:skip


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


    def _convert_to_camel_field_name(self,match_field):
        if match_field.start() == 0:
            return match_field.string[match_field.start():match_field.end()]
        return match_field.group(1).upper()
    def to_internal_value(self, data):
        '''
        将驼峰风格的字段值对应到下划线风格的字段上
        只有显示定义的序列化字段才转换
        '''
        # self._writable_fields字段对应模型字段
        # self._declared_fields字段对应显示序列化类中定义的字段
        for field in self._writable_fields:
            camel_field_name = re.sub(r'_([a-z])', self._convert_to_camel_field_name ,field.source)
            if camel_field_name not in data.keys():
                continue
            data[field.source] = data.pop(camel_field_name)

        return super().to_internal_value(data)
            
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
                camel_field_name = re.sub(r'_([a-z])', self._convert_to_camel_field_name ,field.field_name)
                ret[camel_field_name] = field.to_representation(attribute)

        return ret