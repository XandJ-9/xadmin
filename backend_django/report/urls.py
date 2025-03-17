from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.metadata import TableView, TableColumnView, DatabaseView, TableMappingView, TableColumnMappingView
from .views.interface import PlatformViewSet, ModuleViewSet, InterfaceViewSet, InterfaceFieldViewSet
from .views.importExport import ImportViewSet

router = DefaultRouter()
router.register(r'tables', TableView)
router.register(r'table-columns', TableColumnView)
router.register(r'databases', DatabaseView, basename='database')
router.register(r'table-mappings', TableMappingView)
router.register(r'table-column-mappings', TableColumnMappingView)
router.register(r'platforms', PlatformViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'interfaces', InterfaceViewSet)
router.register(r'interface-fields', InterfaceFieldViewSet)
router.register(r'import', ImportViewSet, basename='import')

urlpatterns = [
    path('report/', include(router.urls)),
]