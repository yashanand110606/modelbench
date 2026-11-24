from django.contrib import admin
from .models import Experiment


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("name", "model_name", "status", "dataset", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "model_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


admin.site.register(Experiment, ExperimentAdmin)
