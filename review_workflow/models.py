from django.db import models
from evaluations.models import Evaluation
from django.contrib.auth.models import User

class Review(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review {self.id} for Evaluation {self.evaluation.id}"
