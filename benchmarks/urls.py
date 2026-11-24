from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BenchmarkViewSet

router = DefaultRouter()
router.register(r'', BenchmarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
