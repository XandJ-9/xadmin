from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,RoleViewSet,MenuViewSet, SystemConfigViewSet, LoginViewSet

router = DefaultRouter()
router.register('', LoginViewSet, basename='login')
router.register('users', UserViewSet)
router.register('roles', RoleViewSet)
router.register('menus', MenuViewSet)
router.register('configs', SystemConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]