from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from.models import User,Project,Screenshot,Bug



    
User = get_user_model()
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),  
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'description')
    search_fields = ('name', 'manager__username')
    list_filter = ('manager',)
    ordering = ('name',)

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

