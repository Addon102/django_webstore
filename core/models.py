from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='categories')

    def __str__(self):
        return self.title

    class Meta:
        # ordering = ['-title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', blank=True, null=True)
    image = models.ImageField(verbose_name='Фото', upload_to='products/', blank=True, null=True)
    views = models.SmallIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.pk})

    def img_preview(self):
        if not self.image:
            return ''
        return mark_safe(f'<img src="{self.image.url}" width="100" height"100">')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ShoppingCart(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товары')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Отзыв')


    def __str__(self):
        return f'{self.author}: {self.product}'


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Favorite(models.Model):
    author = models.ManyToManyField(User, related_name='likesdfsdfgs')
    product = models.ManyToManyField(Product, related_name='products', verbose_name='Товар')

    def __str__(self):
        return self.author


    class Meta:
        verbose_name = 'Избранное'


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
