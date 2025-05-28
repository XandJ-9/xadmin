from rest_framework.filters import BaseFilterBackend


class SearchFilterBackend(BaseFilterBackend):

    def get_search_fields(self, view, request):
        return getattr(view, 'filter_fields', None)
    def filter_queryset(self, request, queryset, view):
        filter_fields = [field.name for field in queryset.model._meta.fields] if self.get_search_fields(view, request) == '__all__' else self.get_search_fields(view, request)
        for field in filter_fields:
            filter_kwargs = {field+'__icontains': request.query_params.get(field, '')}
            queryset = queryset.filter(**filter_kwargs)
        # filter_kwargs = {field.name: request.query_params.get(field.name, None) for field in filter_fields}
        # queryset = queryset.filter(**filter_kwargs)
        return queryset
