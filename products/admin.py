from django.contrib import admin

from .models import ProductCategories, Products


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'category']
    search_fields = ['name']


admin.site.register(Products, ProductAdmin)
admin.site.register(ProductCategories, CategoryAdmin)
