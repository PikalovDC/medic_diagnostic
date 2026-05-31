from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ServiceCategoryViewSet, ServiceViewSet

app_name = 'services'

router = DefaultRouter()
router.register(r'api/categories', ServiceCategoryViewSet)
router.register(r'api/services', ServiceViewSet)

urlpatterns = [
    path('', views.service_list, name='list'),
    path('<slug:slug>/', views.service_detail, name='detail'),
    path('api/', include(router.urls)),
]
