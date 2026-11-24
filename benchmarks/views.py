from rest_framework import viewsets
from .models import Benchmark
from .serializers import BenchmarkSerializer
from core.permissions import IsAdminOrReadOnly


class BenchmarkViewSet(viewsets.ModelViewSet):
    queryset = Benchmark.objects.all()
    serializer_class = BenchmarkSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['name', 'description', 'dataset']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
