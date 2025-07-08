from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('post',PostViewSet)
router.register('dept', DeptViewSet)
router.register('user', UserViewSet)
router.register('role', RoleViewSet)
router.register('menu', MenuViewSet)
router.register('configs', SystemConfigViewSet)
router.register('dict/type', SystemDictTypeViewSet, basename='system-dict-type')
router.register('dict/data', SystemDictDataViewSet, basename='system-dict-data')

urlpatterns = [
    path('system/', include(router.urls)),
    path('captchaImage',UserViewSet.as_view({'get': 'captchaImage',})),
    path('login', UserViewSet.as_view({'post': 'login',}), name='user-login'),
    path('getInfo', UserViewSet.as_view({'get': 'getInfo',})),
    path('register', UserViewSet.as_view({'post': 'register',}), name='user-register'),
    path('logout', UserViewSet.as_view({'post': 'logout',})),
    path('getRouters', MenuViewSet.as_view({'get': 'getRouters',}), name='menu-routers'),
    path('system/dict/data/type/<str:dict_type>', SystemDictDataViewSet.as_view({'get': 'get_data_by_type',})),
    path('system/dept/exclude/<int:dept_id>', DeptViewSet.as_view({'get': 'exclude',})),
    path('system/menu/roleMenuTreeselect/<int:roleId>', MenuViewSet.as_view({'get': 'roleMenuTreeselect',}), name='menu-role-treeselect'),
    path('system/role/deptTree/<int:roleId>', RoleViewSet.as_view({'get': 'deptTree',}))
]
