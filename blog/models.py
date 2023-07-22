
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="заголовок")
    content = models.TextField(verbose_name='содержимое')
    picture = models.ImageField(upload_to="articles", null=True, blank=True)
    views = models.IntegerField(default=0, verbose_name="количество просмотров")
    published = models.DateTimeField(auto_now_add=True, verbose_name="дата публикации")

    def __str__(self):
        return f'Article({self.title})'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'