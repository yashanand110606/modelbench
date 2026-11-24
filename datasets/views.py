from rest_framework import viewsets
from .models import Dataset
from .serializers import DatasetSerializer
from core.permissions import IsAdminOrReadOnly


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']