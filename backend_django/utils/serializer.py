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