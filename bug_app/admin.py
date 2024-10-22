from django.contrib import admin
from .models import Screenshot,Bug

@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('bug', 'image')
    search_fields = ('bug__title',)
    ordering = ('bug',)    

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'reported_by', 'status', 'type', 'deadline')
    search_fields = ('title', 'project__name', 'assigned_to__username', 'reported_by__username')
    list_filter = ('status', 'type', 'project', 'assigned_to')
    ordering = ('title',) 

