from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSourceViewSet , QueryLogViewSet

router = DefaultRouter()
router.register(r'datasources', DataSourceViewSet)
router.register(r'querylogs', QueryLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]