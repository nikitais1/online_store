from django.contrib import admin

from catalog.models import Product, Category, Blog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price_for_one', 'category',)
    list_filter = ('category',)
    search_fields = ('product_name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    list_filter = ('category_name',)
    search_fields = ('category_name', 'description',)


@admin.register(Blog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish',)
    list_filter = ('title',)
    search_fields = ('title', 'is_publish',)
    prepopulated_fields = {'slug': ('title',)}
