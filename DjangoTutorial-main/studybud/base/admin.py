from django.contrib import admin

# Register your models here.

from .models import Job, Field, Message

admin.site.register(Job)
admin.site.register(Field)
admin.site.register(Message)

