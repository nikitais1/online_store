from django.conf import settings
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

    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='владелец')

    def __str__(self):
        return f'{self.product_name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('product_name',)
        permissions = [(
            "change_published_status",
            "Can cancel publication of a product"
        ),
            ("change_product_description",
             "Can change product description"
             ),
            (
                "change_category",
                "Can change category"
            )

        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    number_version = models.PositiveIntegerField(verbose_name='номер версии', **NULLABLE)
    name_version = models.CharField(max_length=150, verbose_name='название версии', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.name_version} {self.number_version}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('name_version',)
