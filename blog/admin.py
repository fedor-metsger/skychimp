
from django.contrib import admin

from blog.models import Article

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "views", "published")
    list_filter = ("title", "published")
    search_fields = ("title", "content")