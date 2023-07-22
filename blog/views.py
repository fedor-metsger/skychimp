
from django.views.generic import DetailView

from blog.models import Article
from blog.services import get_cached_articles

# Create your views here.
class ArticleDetailView(DetailView):
    model = Article
    fields = "__all__"

    def get_context_data(request, *args, **kwargs):
        context = super().get_context_data()
        get_cached_articles(context["object"].pk).update(views=context["object"].views + 1)
        context["object"].views += 1
        return context