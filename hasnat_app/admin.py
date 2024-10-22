from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from.models import User


User = get_user_model()
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),  
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



   



