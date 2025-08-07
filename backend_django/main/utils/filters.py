from rest_framework.filters import BaseFilterBackend
from django.db.models import ForeignKey
from .util_str import underline_to_camel_string

class SearchFilterBackend(BaseFilterBackend):

    def get_search_fields(self, view, request, queryset):
        '''
        获取search_fields. 返回表字段名称，视图中的filter_fields可以是与模型字段一致，也可以是驼峰格式
        '''
        model_field_names = [field.name for field in queryset.model._meta.fields if not isinstance(field, ForeignKey)]
        search_fields = getattr(view, 'filter_fields')
        return [field for field in model_field_names] if search_fields == '__all__' \
            else [field for field in model_field_names if field in search_fields or underline_to_camel_string(field) in search_fields]
            
    
    def filter_queryset(self, request, queryset, view):
        filter_fields = self.get_search_fields(view, request, queryset)
        for field in filter_fields:
            field_value = request.query_params.get(field, None) if field in request.query_params else request.query_params.get(underline_to_camel_string(field), None)
            if field_value:
                filter_kwargs = {field+'__icontains': field_value}
                queryset = queryset.filter(**filter_kwargs)
        return queryset
