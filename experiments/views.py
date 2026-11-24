from rest_framework import viewsets
from .models import Experiment
from .serializers import ExperimentSerializer
from core.permissions import IsAdminOrReadOnly


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['name', 'model_name', 'status', 'dataset']
    search_fields = ['name', 'model_name']
    ordering_fields = ['name', 'model_name', 'status', 'created_at']
    ordering = ['-created_at']
