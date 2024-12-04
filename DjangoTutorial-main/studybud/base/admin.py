from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Job, Field, Message, UserProfile


# Register your models
admin.site.register(Job)
admin.site.register(Field)
admin.site.register(Message)

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('user_type', 'profile_picture', 'resume')
    
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_user_type(self, obj):
        if hasattr(obj, 'userprofile') and obj.userprofile:
            return obj.userprofile.user_type.capitalize()
        return 'N/A'

    get_user_type.short_description = 'User Type'

# Unregister default User admin and register custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)