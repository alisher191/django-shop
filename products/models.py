from django.db import models
from django.contrib.auth.models import User


class ProductCategories(models.Model):
    name = models.CharField(max_length=150, verbose_name='Category name')
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Products(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products_image/', null=True, blank=True)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategories, on_delete=models.PROTECT)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)
    

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Basket for {self.user.username} | Product: {self.product.name}'
    
    def sum(self):
        return self.product.price * self.quantity
    