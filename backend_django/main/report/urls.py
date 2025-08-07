from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PlatformInfoViewSet,
    ModuleInfoViewSet,
    ReportInfoViewSet,
    InterfaceInfoViewSet,
    InterfaceFieldViewSet,
    InterfaceImportExportViewSet,
    InterfaceQueryViewSet,
    InterfaceQueryLogViewSet
)

router = DefaultRouter()
router.register(r'platforms', PlatformInfoViewSet)
router.register(r'modules', ModuleInfoViewSet)
router.register(r'reports', ReportInfoViewSet)
router.register(r'interfaces', InterfaceInfoViewSet)
router.register(r'interface-fields', InterfaceFieldViewSet)
# router.register(r'', ImportExportViewSet, basename='import-export')
# router.register(r'', InterfaceQueryViewSet, basename='interface-query')
router.register(r'interface-logs', InterfaceQueryLogViewSet, basename='interface-logs')

urlpatterns = [
    path('report/', include(router.urls)),
    path('report/interface-export/', InterfaceImportExportViewSet.as_view({'post':'export_interfaceinfo'}), name='interface-export'),
    path('report/interface-import/', InterfaceImportExportViewSet.as_view({'post':'import_interfaceinfo'}), name='interface-import'),
    path('report/interface-query/', InterfaceQueryViewSet.as_view({'post':'query_interface'}), name='interface-query'),
]