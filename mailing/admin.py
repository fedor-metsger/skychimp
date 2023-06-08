from django.contrib import admin

from .models import Client, Task
# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "period",)
    list_filter = ("period",)
    search_fields = ("title", "subject",)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email",)
    search_fields = ("name", "description",)