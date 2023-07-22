
from django.urls import path

from blog.views import ArticleDetailView

app_name = 'blog'

urlpatterns = [
    path('<int:pk>/', ArticleDetailView.as_view(), name='detail')
]