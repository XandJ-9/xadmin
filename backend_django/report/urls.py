from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlatformInfoViewSet,
    ModuleInfoViewSet,
    ReportInfoViewSet,
    InterfaceInfoViewSet,
    InterfaceFieldViewSet,
    ImportExportViewSet
)

router = DefaultRouter()
router.register(r'platforms', PlatformInfoViewSet)
router.register(r'modules', ModuleInfoViewSet)
router.register(r'reports', ReportInfoViewSet)
router.register(r'interfaces', InterfaceInfoViewSet)
router.register(r'interface-fields', InterfaceFieldViewSet)
router.register(r'', ImportExportViewSet, basename='import-export')

urlpatterns = [
    path('report/', include(router.urls)),
]