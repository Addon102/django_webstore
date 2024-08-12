from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['pk', 'title']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'views', 'author', 'category', 'img_preview', 'price']
    list_display_links = ['pk', 'title']
    list_editable = ['author', 'category']
    readonly_fields = ['views']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'text', 'author', 'product']
    list_display_links = ['pk', 'text']
    list_editable = ['author', 'product']

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Comment, CommentAdmin)
