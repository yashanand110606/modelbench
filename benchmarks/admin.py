from django.contrib import admin
from .models import Benchmark


class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ("name", "dataset", "created_at", "updated_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


admin.site.register(Benchmark, BenchmarkAdmin)
