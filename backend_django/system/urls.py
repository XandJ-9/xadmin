from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,RoleViewSet,MenuViewSet, SystemConfigViewSet,SystemDictTypeViewSet,SystemDictDataViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('roles', RoleViewSet)
router.register('menus', MenuViewSet)
router.register('configs', SystemConfigViewSet)
router.register('dict/type/', SystemDictTypeViewSet, basename='system-dict-type')
router.register('dict/data/', SystemDictDataViewSet, basename='system-dict-data')

urlpatterns = [
    path('system/', include(router.urls)),
    path('captchaImage',UserViewSet.as_view({'get': 'captchaImage',})),
    path('login', UserViewSet.as_view({'post': 'login',})),
    path('getInfo', UserViewSet.as_view({'get': 'getInfo',})),
    path('register', UserViewSet.as_view({'post': 'register',})),
    path('logout', UserViewSet.as_view({'post': 'logout',})),
    path('getRouters', MenuViewSet.as_view({'get': 'getRouters',}))
]