from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("evaluation", "reviewer", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("comments", "evaluation__id")
    readonly_fields = ("created_at", "updated_at")

admin.site.register(Review, ReviewAdmin)
