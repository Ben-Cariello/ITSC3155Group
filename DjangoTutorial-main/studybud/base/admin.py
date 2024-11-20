from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Job, Field, Message, UserProfile

# Register your models
admin.site.register(Job)
admin.site.register(Field)
admin.site.register(Message)

# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Details'

# Custom UserAdmin that includes UserProfile
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_user_type(self, obj):
        return obj.userprofile.user_type if hasattr(obj, 'userprofile') else 'N/A'
    get_user_type.short_description = 'User Type'

# Unregister default User admin and register custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)