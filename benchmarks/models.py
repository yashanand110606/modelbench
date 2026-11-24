from django.db import models
from datasets.models import Dataset


class Benchmark(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dataset = models.OneToOneField(
        Dataset, on_delete=models.CASCADE, related_name="benchmark"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
