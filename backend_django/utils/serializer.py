import copy, re
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict


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
        declared_fields = copy.deepcopy(self._declared_fields)
        for field_name in declared_fields:
            field = declared_fields[field_name]
            camel_field_name = re.sub(r'_([a-z])', self._convert_to_camel_field_name ,field.source)
            if camel_field_name in data.keys():
                # 将字段中下划线和其后面首字母转为大写
                # 定位下划线及其后第一个字符
                # camel_field_name = field.source.replace('_', '').replace(field.source[field.source.find('_') + 1],field.source[field.source.find('_') + 1].upper())
                data[field.source] = data.pop(camel_field_name)
        return super().to_internal_value(data)
            