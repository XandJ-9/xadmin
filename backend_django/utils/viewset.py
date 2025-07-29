from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from system.permissions import IsOwnerOrAdmin,IsAdminUser, HasRolePermission, has_perms
from .util_response import SuccessResponse, ErrorResponse, DetailResponse
from .filters import SearchFilterBackend
from inspect import getmembers


class CustomModelViewSet(ModelViewSet):
    values_queryset = None
    ordering_fields = '__all__'
    create_serializer_class = None
    update_serializer_class = None
    filter_fields = '__all__'
    filter_backends = [DjangoFilterBackend,SearchFilterBackend]  
    # SearchFilter, OrderingFilter,SearchFilterBackend

    search_fields = ()
    perms_map = None

    # pagination_class = CustomPagination

    # @property
    # def perms_map(self):
    #     """
    #     获取权限映射表
    #     """
    #     if self._perms_map is not None:
    #         return self._perms_map
    #     self._perms_map = {}
    #     # 获取所有方法的权限
    #     for name, method in getmembers(self, lambda x: hasattr(x, 'perms') and isinstance(x.perms,list)):
    #         self._perms_map[method.__name__] = method.perms
    #     return self._perms_map

    def get_perms_map(self):
        """
        获取权限映射表
        """
        if self.perms_map is None:
            self.perms_map = {}
        # 获取所有方法的权限
        for name, method in getmembers(self, lambda x: hasattr(x, 'perms') and isinstance(x.perms,list)):
            self.perms_map[method.__name__] = method.perms
        return self.perms_map
    
    # def get_permissions(self):
        # if self.action in ['list']:
            # return [AllowAny()]
        # return [IsOwnerOrAdmin()]
    
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

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        # 添加通用处理逻辑, 例如根据action的类型处理自定义不同处理逻辑
        # self.action = 'create'
        super().perform_create(serializer)


    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            return ErrorResponse(msg=str(e))
        return DetailResponse(data=serializer.data, msg="新增成功")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 这里先序列化，再分页，数据量大的情况下不可取，需要优化
        ser = self.get_serializer(queryset, many=True)
        noPage = request.query_params.get('noPage', "0")
        
        if noPage == '1':
            return DetailResponse(data=ser.data)
        else:
            page_no = request.query_params.get('pageNum', 1)
            page_size = request.query_params.get('pageSize',10)
            p = Paginator(ser.data, page_size)
            page_obj = p.get_page(page_no)
            page_data = page_obj.object_list
            return SuccessResponse(data=page_data, total=p.count,page=page_obj.number,limit=p.per_page)
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
        return DetailResponse(data=serializer.data)

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            # instance._prefetched_objects_cache = {}
        return DetailResponse(data=serializer.data)

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
            # return ErrorResponse(msg="Not Found", status=status.HTTP_404_NOT_FOUND)
            return DetailResponse(msg="未找到要删除的数据")
        # 遍历queryset删除
        for instance in queryset:
            self.check_object_permissions(request, instance)
            instance.delete()
        # 如果是单个对象
        # instance = self.get_object()
        # instance.delete()
        return DetailResponse(msg=f'删除成功，共删除{len(queryset)}条数据')
    

    @action(methods=['get'], detail=False)
    def list_all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return DetailResponse(data=serializer.data)