from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('category_name',)


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='product/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 **NULLABLE)
    price_for_one = models.IntegerField(verbose_name='Цена за штуку', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_modified_date = models.DateTimeField(auto_now=True,
                                              verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.product_name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('product_name',)


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', **NULLABLE)
    slug = models.CharField(max_length=100, verbose_name='URL', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='blog/', verbose_name='Превью', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_publish = models.BooleanField(default=True, verbose_name='Признак публикации')
    count_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title})'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('title',)
