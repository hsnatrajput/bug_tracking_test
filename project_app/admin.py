from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'description')
    search_fields = ('name', 'manager__username')
    list_filter = ('manager',)
    ordering = ('name',)
