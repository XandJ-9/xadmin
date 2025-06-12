from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from system.permissions import IsOwnerOrAdmin,IsAdminUser, HasRolePermission
from .util_response import SuccessResponse, ErrorResponse, DetailResponse
from .import_export_mixin import ExportSerializerMixin, ImportSerializerMixin
import logging

logger = logging.getLogger('django')


class CustomModelViewSet(ExportSerializerMixin, ImportSerializerMixin,ModelViewSet):
    values_queryset = None
    ordering_fields = '__all__'
    create_serializer_class = None
    update_serializer_class = None
    filter_fields = '__all__'
    search_fields = ()

    # pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return [IsOwnerOrAdmin()]
    
    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) or []):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        return super().get_queryset()


    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs.setdefault('context', self.get_serializer_context())
    #     if self.action == 'create':
    #         kwargs['creator'] = self.request.user
    #         kwargs['updator'] = self.request.user
    #     else:
    #         kwargs['updator'] = self.request.user
    #     return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        # return super().perform_create(serializer)
        if self.request.user and self.request.user.is_authenticated:
            serializer.validated_data['creator'] = self.request.user
        super().perform_create(serializer)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 这里先序列化，再分页，数据量大的情况下不可取，需要优化
        ser = self.get_serializer(queryset, many=True)
        noPage = request.query_params.get('noPage', "0")
        
        if noPage == '1':
            return DetailResponse(data=ser.data, msg="获取数据")
        else:
            page_no = request.query_params.get('pageNum', 1)
            page_size = request.query_params.get('pageSize',10)
            p = Paginator(ser.data, page_size)
            page_obj = p.get_page(page_no)
            page_data = page_obj.object_list
            return SuccessResponse(data=page_data, total=p.count,page=page_obj.number,limit=p.per_page, msg="获取成功")
        # page = self.paginate_queryset(queryset)
        # p = Paginator(serializer_data, page_size)
        # if p is not None:
        #     # serializer = self.get_serializer(page, many=True)
        #     # return self.get_paginated_response(serializer.data)
        #     return SuccessResponse(data=p.get_page(page_size).object_list, msg="获取成功", page=page_no, limit=page_size, total=p.count)
        # return SuccessResponse(data=serializer.data, msg="获取成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DetailResponse(data=serializer.data, msg="获取成功")

    def perform_update(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            serializer.validated_data['updator'] = self.request.user
        super().perform_update(serializer)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if request.user:
            serializer.validated_data['updator'] = request.user
        self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            # instance._prefetched_objects_cache = {}
        return DetailResponse(data=serializer.data, msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        """
        自定义修改，支持多条删除
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        if isinstance(filter_kwargs[self.lookup_field], str):
            filter_kwargs[self.lookup_field] = filter_kwargs[self.lookup_field].split(',')
            queryset = self.filter_queryset(self.get_queryset().filter(**{self.lookup_field + '__in': filter_kwargs[self.lookup_field]}))
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(**filter_kwargs))
        if not queryset:
            return ErrorResponse(msg="删除失败，数据不存在", status=status.HTTP_404_NOT_FOUND)
        # 遍历queryset删除
        for instance in queryset:
            self.check_object_permissions(request, instance)
            instance.delete()
        # 如果是单个对象
        # instance = self.get_object()
        # instance.delete()
        return DetailResponse(data=[], msg="删除成功")
    

    @action(methods=['get'], detail=False)
    def list_all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return DetailResponse(data=serializer.data, msg="获取成功")