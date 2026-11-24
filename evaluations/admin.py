from django.contrib import admin
from .models import Evaluation


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("experiment", "metric", "score", "created_at")
    list_filter = ("metric", "created_at")
    search_fields = ("experiment__name",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


admin.site.register(Evaluation, EvaluationAdmin)
