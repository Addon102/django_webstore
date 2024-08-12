from django import template
from core.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all


@register.simple_tag()
def is_category_current(request, category_id):
    return str(category_id) in request.path


@register.simple_tag()
def is_liked(request, product):
    user = request.user
    liked_users = product.likes.user.all()
    return user in liked_users
