import csv
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Evaluation
from .serializers import EvaluationSerializer
from core.permissions import IsAdminOrReadOnly


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['experiment', 'metric']
    search_fields = ['experiment__name', 'experiment__model_name']
    ordering_fields = ['score', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="evaluations.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Experiment', 'Metric', 'Score', 'Created At'])

        for evaluation in self.queryset.all():
            writer.writerow([
                evaluation.id,
                evaluation.experiment.name,
                evaluation.metric,
                evaluation.score,
                evaluation.created_at
            ])

        return response
