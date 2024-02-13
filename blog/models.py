from django.db import models

from catalog.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', **NULLABLE)
    slug = models.CharField(max_length=100, verbose_name='URL', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='blog/', verbose_name='Превью', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_publish = models.BooleanField(default=True, verbose_name='Признак публикации')
    count_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('title',)
