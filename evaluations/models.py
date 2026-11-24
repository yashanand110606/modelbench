from django.db import models
from experiments.models import Experiment


class Evaluation(models.Model):
    class Metric(models.TextChoices):
        ACCURACY = "accuracy", "Accuracy"
        BLEU = "bleu", "BLEU"
        ROUGE = "rouge", "ROUGE"
        F1 = "f1", "F1 Score"
        HELPFULNESS = "helpfulness", "Helpfulness"

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="evaluations"
    )
    metric = models.CharField(max_length=50, choices=Metric.choices)
    score = models.FloatField()
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.experiment.name} - {self.metric}: {self.score}"
