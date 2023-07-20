from django.contrib import admin

from .models import Client, Task, Interval
# Register your models here.
class IntervalInline(admin.StackedInline):
    model = Interval
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "period",)
    list_filter = ("period",)
    search_fields = ("title", "subject",)
    inlines = [IntervalInline]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email",)
    search_fields = ("name", "description",)
