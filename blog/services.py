
from django.conf import settings
from django.core.cache import cache

from blog.models import Article
def get_cached_articles(art_id):
    if settings.LOW_CACHED:
        key = f'articles_list_{art_id}'
        art_list = cache.get(key)
        if art_list is None:
            art_list = Article.objects.filter(pk=art_id)
            cache.set(key, art_list)
    else:
        art_list = Article.objects.filter(pk=art_id)

    return art_list