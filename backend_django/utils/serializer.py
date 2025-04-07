from rest_framework import serializers
from rest_framework.utils.serializer_helpers import BindingDict


def set_choice_field_internal_value(fields: BindingDict, field_name: str, data: dict):
    field = fields[field_name]
    if not isinstance(field, serializers.ChoiceField):  # 判断是否为ChoiceField
        return 
    if field_name not in data.keys():
        return 
    for internal_value, value in field.choices.items():
        # print(internal_value, value)
        # 将传入的choice字段值修改为数据库中存储的内容
        if data.get(field_name) == value:
            data[field_name]= internal_value